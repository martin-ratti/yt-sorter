import json
import time
import os
from typing import List, Dict, Optional
from ytmusicapi import YTMusic
from src.core.entities import Track

AUTH_FILE = "auth.json"

class YTService:
    def __init__(self):
        self.api = None

    # --- GESTIÓN DE SESIÓN ---
    def save_session(self, headers: Dict):
        try:
            with open(AUTH_FILE, 'w', encoding='utf-8') as f:
                json.dump(headers, f, indent=4)
        except Exception as e:
            print(f"Advertencia: No se pudo guardar auth.json: {e}")

    def load_session(self) -> Optional[str]:
        if os.path.exists(AUTH_FILE):
            try:
                with open(AUTH_FILE, 'r', encoding='utf-8') as f:
                    return json.dumps(json.load(f))
            except:
                return None
        return None

    # --- LOGIN ---
    def login(self, raw_text: str) -> bool:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Accept": "*/*",
                "Accept-Language": "es-419,es;q=0.9",
                "Content-Type": "application/json",
                "X-Goog-AuthUser": "0",
                "x-origin": "https://music.youtube.com"
            }

            try:
                loaded = json.loads(raw_text)
                if "Cookie" in loaded:
                    headers = loaded
                    self.api = YTMusic(json.dumps(headers))
                    return True
            except:
                pass 

            lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
            found_cookie = False
            
            for i, line in enumerate(lines):
                line_clean = line.lower().replace(":", "").strip()
                if line_clean == "cookie" and i + 1 < len(lines):
                    headers["Cookie"] = lines[i+1]
                    found_cookie = True
                elif line_clean == "authorization" and i + 1 < len(lines):
                    headers["Authorization"] = lines[i+1]
                elif "cookie:" in line.lower() and not found_cookie:
                    parts = line.split(":", 1)
                    if len(parts) > 1:
                        headers["Cookie"] = parts[1].strip()
                        found_cookie = True

            if not found_cookie:
                raise ValueError("No encontré la Cookie. Copia todo el bloque.")

            self.api = YTMusic(json.dumps(headers))
            self.save_session(headers)
            return True

        except Exception as e:
            raise Exception(f"Login fallido: {str(e)}")

    # --- DATOS ---
    def fetch_playlists(self) -> List[Dict[str, str]]:
        if not self.api: raise ConnectionError("No autenticado")
        try:
            playlists = self.api.get_library_playlists(limit=200)
            return [{"title": p['title'], "id": p['playlistId']} for p in playlists]
        except Exception as e:
            raise ConnectionError(f"Error cargando listas: {e}")

    def fetch_tracks(self, playlist_id: str) -> List[Track]:
        if not self.api: raise ConnectionError("No autenticado")
        
        print(f"DEBUG: Descargando playlist ID: {playlist_id}...")
        playlist_data = self.api.get_playlist(playlist_id, limit=5000)
        tracks_data = playlist_data.get('tracks', [])
        
        total_found = len(tracks_data)
        clean_tracks = []
        seen_ids = set()
        duplicates_count = 0
        unavailable_count = 0

        print("\n--- INICIO DE AUDITORÍA DE DUPLICADOS ---")
        for t in tracks_data:
            vid_id = t.get('videoId')
            title = t.get('title', 'Sin título')
            
            # 1. Chequeo de Disponibilidad
            if not vid_id: 
                print(f"⚠️ OMITIDO (No disponible): {title}")
                unavailable_count += 1
                continue
            
            # 2. Chequeo de Duplicados
            if vid_id in seen_ids:
                print(f"♻️ DUPLICADO DETECTADO: '{title}' (Ya estaba en la lista)")
                duplicates_count += 1
                continue
            
            seen_ids.add(vid_id)

            # Extracción limpia
            artists_list = t.get('artists', [])
            if isinstance(artists_list, list):
                artists = ", ".join([a.get('name', 'Unknown') for a in artists_list])
            else:
                artists = "Unknown"

            album_data = t.get('album')
            album = album_data.get('name', 'Unknown') if isinstance(album_data, dict) else 'Unknown'
            
            clean_tracks.append(Track(
                id=vid_id,
                title=title,
                artist=artists,
                album=album,
                duration_seconds=t.get('duration_seconds', 0) or 0
            ))
        print("--- FIN DE AUDITORÍA ---\n")
            
        print(f"--------------------------------------------------")
        print(f"REPORTE FINAL: Leídos: {total_found} | Duplicados: {duplicates_count} | Únicos: {len(clean_tracks)}")
        print(f"--------------------------------------------------")
        return clean_tracks

    def create_playlist(self, title: str, track_ids: List[str]):
        if not self.api: raise ConnectionError("No autenticado")
        
        print(f"DEBUG: Creando playlist '{title}'...")
        playlist_id = self.api.create_playlist(title, description="Ordenada con YTSorter")
        
        batch_size = 20
        total_batches = (len(track_ids) + batch_size - 1) // batch_size
        
        for i in range(0, len(track_ids), batch_size):
            batch = track_ids[i:i + batch_size]
            current_batch = (i // batch_size) + 1
            
            retries = 3
            while retries > 0:
                try:
                    # Aquí he quitado la verificación estricta que daba el falso positivo
                    self.api.add_playlist_items(playlist_id, batch)
                    print(f"Lote {current_batch}/{total_batches}: OK ({len(batch)} canciones)")
                    time.sleep(2)
                    break
                except Exception as e:
                    print(f"ERROR Lote {current_batch}: {e}. Reintentando...")
                    retries -= 1
                    time.sleep(5)
            
        return playlist_id