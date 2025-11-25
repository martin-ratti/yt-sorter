import json
import time
import os
import re
from typing import List, Dict, Optional, Callable
from ytmusicapi import YTMusic
from src.core.entities import Track

AUTH_FILE = "auth.json"

class YTService:
    def __init__(self):
        self.api = None

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

    def login(self, raw_text: str) -> bool:
        try:
            # 1. Intento JSON directo (Auto-login)
            try:
                loaded = json.loads(raw_text)
                if "Cookie" in loaded:
                    self.api = YTMusic(json.dumps(loaded))
                    return True
            except:
                pass 

            # 2. PARSEO QUIRÚRGICO (WHITELIST)
            # Solo permitimos estos headers específicos. El resto se ignora.
            allowed_headers = {
                "cookie": "Cookie",
                "x-goog-authuser": "X-Goog-AuthUser",
                "x-goog-visitor-id": "X-Goog-Visitor-Id",
                "authorization": "Authorization",
                "user-agent": "User-Agent",
                "accept-language": "Accept-Language"
            }
            
            clean_headers = {}
            
            # Inyectamos un User-Agent por defecto por seguridad
            clean_headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            clean_headers["Accept"] = "*/*"
            clean_headers["Content-Type"] = "application/json"
            clean_headers["X-Origin"] = "https://music.youtube.com"

            # Procesamos línea por línea
            lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
            
            # Iteramos buscando pares Clave-Valor
            # Soporta formato Chrome (Línea 1: Clave, Línea 2: Valor) y formato Raw (Clave: Valor)
            i = 0
            while i < len(lines):
                line = lines[i]
                
                # Detectar si la línea es una clave válida de nuestra lista blanca
                # Quitamos los dos puntos para comparar (ej: "cookie:" -> "cookie")
                key_candidate = line.lower().replace(":", "").strip()
                
                if key_candidate in allowed_headers:
                    # ¡Encontramos uno válido!
                    real_key_name = allowed_headers[key_candidate]
                    
                    # Buscamos el valor...
                    value = ""
                    
                    # Caso A: Formato "Clave: Valor" en la misma línea
                    if ":" in line and not line.strip().endswith(":"):
                        parts = line.split(":", 1)
                        value = parts[1].strip()
                        i += 1 # Pasamos a la siguiente línea
                        
                    # Caso B: Formato Chrome (Valor en la siguiente línea)
                    elif i + 1 < len(lines):
                        value = lines[i+1].strip()
                        i += 2 # Saltamos clave y valor
                    else:
                        i += 1 # Línea huérfana, ignorar

                    # Guardamos el header limpio
                    if value:
                        clean_headers[real_key_name] = value
                        
                else:
                    # Si no es un header conocido, lo ignoramos (aquí cae el Content-Length y el texto basura)
                    i += 1

            # Validación Final
            if "Cookie" not in clean_headers:
                # Último intento: ¿El usuario pegó SOLO la cookie?
                if "VISITOR_INFO" in raw_text:
                    clean_headers["Cookie"] = raw_text.strip()
                else:
                    raise ValueError("No se encontró la 'Cookie'. Asegúrate de copiar los Request Headers.")

            # Inicializar API
            self.api = YTMusic(json.dumps(clean_headers))
            self.save_session(clean_headers)
            return True

        except Exception as e:
            raise Exception(f"Error de Auth: {str(e)}")

    def fetch_playlists(self) -> List[Dict[str, str]]:
        if not self.api: raise ConnectionError("No autenticado")
        try:
            # Limitamos a 500 por si tienes muchísimas
            playlists = self.api.get_library_playlists(limit=500)
            return [{"title": p['title'], "id": p['playlistId']} for p in playlists]
        except Exception as e:
            # Este mensaje saldrá en la GUI si falla
            raise ConnectionError(f"Google rechazó la conexión. {e}")

    def fetch_tracks(self, playlist_id: str) -> List[Track]:
        if not self.api: raise ConnectionError("No autenticado")
        
        playlist_data = self.api.get_playlist(playlist_id, limit=None) # None intenta traer todo
        tracks_data = playlist_data.get('tracks', [])
        
        clean_tracks = []
        seen_ids = set()
        
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
                original_index=i
            ))
        return clean_tracks

    def create_playlist(self, title: str, track_ids: List[str], progress_callback: Callable[[str, float], None] = None):
        if not self.api: raise ConnectionError("No autenticado")
        
        playlist_id = self.api.create_playlist(title, description="Ordenada con YTSorter")
        
        batch_size = 20
        total_batches = (len(track_ids) + batch_size - 1) // batch_size
        
        for i in range(0, len(track_ids), batch_size):
            batch = track_ids[i:i + batch_size]
            current_batch = (i // batch_size) + 1
            
            if progress_callback:
                percent = current_batch / total_batches
                progress_callback(f"Subiendo lote {current_batch}/{total_batches}...", percent)
            
            retries = 3
            while retries > 0:
                try:
                    self.api.add_playlist_items(playlist_id, batch)
                    time.sleep(2) 
                    break
                except Exception as e:
                    print(f"Error {e}, reintentando...")
                    retries -= 1
                    time.sleep(5)
            
        return playlist_id