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

    def save_session(self, headers: Dict):
        """Guarda la sesión localmente para futuros accesos."""
        try:
            with open(AUTH_FILE, 'w', encoding='utf-8') as f:
                json.dump(headers, f, indent=4)
        except Exception as e:
            print(f"Warning: No se pudo guardar sesión: {e}")

    def load_session(self) -> Optional[str]:
        """Carga la sesión guardada si existe."""
        if os.path.exists(AUTH_FILE):
            try:
                with open(AUTH_FILE, 'r', encoding='utf-8') as f:
                    return json.dumps(json.load(f))
            except:
                return None
        return None

    def login(self, raw_text: str) -> bool:
        """Procesa headers crudos o JSON para autenticar."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Accept": "*/*",
                "Accept-Language": "es-419,es;q=0.9",
                "Content-Type": "application/json",
                "X-Goog-AuthUser": "0",
                "x-origin": "https://music.youtube.com"
            }

            # 1. Intento carga directa JSON
            try:
                loaded = json.loads(raw_text)
                if "Cookie" in loaded:
                    headers = loaded
                    self.api = YTMusic(json.dumps(headers))
                    return True
            except:
                pass 

            # 2. Parseo de texto crudo (Headers copiados)
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
                raise ValueError("Cookie no encontrada en los headers proporcionados.")

            self.api = YTMusic(json.dumps(headers))
            self.save_session(headers)
            return True

        except Exception as e:
            raise Exception(f"Fallo de autenticación: {str(e)}")

    def fetch_playlists(self) -> List[Dict[str, str]]:
        if not self.api: raise ConnectionError("No autenticado")
        try:
            playlists = self.api.get_library_playlists(limit=200)
            return [{"title": p['title'], "id": p['playlistId']} for p in playlists]
        except Exception as e:
            raise ConnectionError(f"Error obteniendo playlists: {e}")

    def fetch_tracks(self, playlist_id: str) -> List[Track]:
        """Obtiene canciones, filtra duplicados y valida disponibilidad."""
        if not self.api: raise ConnectionError("No autenticado")
        
        print(f"DEBUG: Descargando ID {playlist_id}...")
        playlist_data = self.api.get_playlist(playlist_id, limit=5000)
        tracks_data = playlist_data.get('tracks', [])
        
        clean_tracks = []
        seen_ids = set()
        
        # Auditoría y limpieza
        for t in tracks_data:
            vid_id = t.get('videoId')
            if not vid_id: continue # Omitir no disponibles
            if vid_id in seen_ids: continue # Omitir duplicados exactos
            
            seen_ids.add(vid_id)

            # Extracción segura de metadatos
            artists_list = t.get('artists', [])
            artists = ", ".join([a.get('name', 'Unknown') for a in artists_list]) if isinstance(artists_list, list) else "Unknown"
            
            album_data = t.get('album')
            album = album_data.get('name', 'Unknown') if isinstance(album_data, dict) else 'Unknown'
            
            clean_tracks.append(Track(
                id=vid_id,
                title=t.get('title', 'Unknown Title'),
                artist=artists,
                album=album,
                duration_seconds=t.get('duration_seconds', 0) or 0
            ))
            
        return clean_tracks

    def create_playlist(self, title: str, track_ids: List[str]):
        """Crea playlist y sube canciones en lotes controlados."""
        if not self.api: raise ConnectionError("No autenticado")
        
        print(f"DEBUG: Creando '{title}'...")
        playlist_id = self.api.create_playlist(title, description="Ordenada con YTSorter")
        
        # Configuración "Safe Mode" para evitar bloqueos
        batch_size = 10 
        total_batches = (len(track_ids) + batch_size - 1) // batch_size
        
        for i in range(0, len(track_ids), batch_size):
            batch = track_ids[i:i + batch_size]
            current_batch = (i // batch_size) + 1
            
            retries = 3
            while retries > 0:
                try:
                    self.api.add_playlist_items(playlist_id, batch)
                    print(f"Lote {current_batch}/{total_batches}: OK")
                    time.sleep(2) # Pausa obligatoria
                    break
                except Exception as e:
                    print(f"Error en lote {current_batch}: {e}. Reintentando...")
                    retries -= 1
                    time.sleep(5)
            
        return playlist_id