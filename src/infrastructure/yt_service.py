import json
import time
import os
import re # <--- Nuevo: Regex
from typing import List, Dict, Optional, Callable
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
            print(f"Warning: No se pudo guardar sesión: {e}")

    def load_session(self) -> Optional[str]:
        if os.path.exists(AUTH_FILE):
            try:
                with open(AUTH_FILE, 'r', encoding='utf-8') as f:
                    return json.dumps(json.load(f))
            except:
                return None
        return None

    # --- LOGIN MEJORADO CON REGEX ---
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

            # 1. Intento JSON directo
            try:
                loaded = json.loads(raw_text)
                if "Cookie" in loaded:
                    headers = loaded
                    self.api = YTMusic(json.dumps(headers))
                    return True
            except:
                pass 

            # 2. Parseo Robusto con Regex
            # Busca "Cookie" seguido de : y captura todo hasta el final de linea
            cookie_match = re.search(r"(?i)cookie[:=]\s*(.+)", raw_text)
            auth_match = re.search(r"(?i)authorization[:=]\s*(.+)", raw_text)

            if cookie_match:
                headers["Cookie"] = cookie_match.group(1).strip()
            else:
                # Fallback manual por si el regex falla
                if "VISITOR" in raw_text:
                     headers["Cookie"] = raw_text.strip()
                else:
                     raise ValueError("No encontré la Cookie. Asegúrate de copiar el bloque completo.")

            if auth_match:
                headers["Authorization"] = auth_match.group(1).strip()

            self.api = YTMusic(json.dumps(headers))
            self.save_session(headers)
            return True

        except Exception as e:
            raise Exception(f"Fallo de autenticación: {str(e)}")

    # --- DATOS ---
    def fetch_playlists(self) -> List[Dict[str, str]]:
        if not self.api: raise ConnectionError("No autenticado")
        try:
            playlists = self.api.get_library_playlists(limit=200)
            return [{"title": p['title'], "id": p['playlistId']} for p in playlists]
        except Exception as e:
            raise ConnectionError(f"Error obteniendo playlists: {e}")

    def fetch_tracks(self, playlist_id: str) -> List[Track]:
        if not self.api: raise ConnectionError("No autenticado")
        
        print(f"DEBUG: Descargando ID {playlist_id}...")
        playlist_data = self.api.get_playlist(playlist_id, limit=5000)
        tracks_data = playlist_data.get('tracks', [])
        
        clean_tracks = []
        seen_ids = set()
        
        # Ahora guardamos el índice original (i)
        for i, t in enumerate(tracks_data):
            vid_id = t.get('videoId')
            if not vid_id: continue 
            if vid_id in seen_ids: continue
            
            seen_ids.add(vid_id)

            artists_list = t.get('artists', [])
            artists = ", ".join([a.get('name', 'Unknown') for a in artists_list]) if isinstance(artists_list, list) else "Unknown"
            
            album_data = t.get('album')
            album = album_data.get('name', 'Unknown') if isinstance(album_data, dict) else 'Unknown'
            
            clean_tracks.append(Track(
                id=vid_id,
                title=t.get('title', 'Unknown Title'),
                artist=artists,
                album=album,
                duration_seconds=t.get('duration_seconds', 0) or 0,
                original_index=i # Guardamos posición original
            ))
            
        return clean_tracks

    def create_playlist(self, title: str, track_ids: List[str], progress_callback: Callable[[str, float], None] = None):
        """
        Crea playlist.
        progress_callback: Función que recibe (mensaje, porcentaje) para actualizar la GUI.
        """
        if not self.api: raise ConnectionError("No autenticado")
        
        playlist_id = self.api.create_playlist(title, description="Ordenada con YTSorter")
        
        batch_size = 10 
        total_batches = (len(track_ids) + batch_size - 1) // batch_size
        
        for i in range(0, len(track_ids), batch_size):
            batch = track_ids[i:i + batch_size]
            current_batch = (i // batch_size) + 1
            
            # Notificar progreso a la GUI
            if progress_callback:
                percent = current_batch / total_batches
                msg = f"Subiendo lote {current_batch}/{total_batches}..."
                progress_callback(msg, percent)
            
            retries = 3
            while retries > 0:
                try:
                    self.api.add_playlist_items(playlist_id, batch)
                    time.sleep(2) 
                    break
                except Exception as e:
                    print(f"Error lote {current_batch}: {e}")
                    retries -= 1
                    time.sleep(5)
            
        return playlist_id