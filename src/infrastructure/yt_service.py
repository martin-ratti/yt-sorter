import json
from typing import List, Dict
from ytmusicapi import YTMusic
from src.core.entities import Track

class YTService:
    def __init__(self):
        self.api = None
        self.user_playlists = []

    def login(self, headers_raw: str) -> bool:
        \"\"\"Intenta autenticarse con los headers proporcionados.\"\"\"
        try:
            headers = json.loads(headers_raw)
            self.api = YTMusic(json.dumps(headers))
            return True
        except Exception as e:
            print(f'Error de Login: {e}')
            return False

    def fetch_playlists(self) -> List[Dict[str, str]]:
        \"\"\"Obtiene las playlists creadas por el usuario.\"\"\"
        if not self.api:
            raise ConnectionError('No autenticado')
        
        playlists = self.api.get_library_playlists(limit=50)
        return [{'title': p['title'], 'id': p['playlistId']} for p in playlists]

    def fetch_tracks(self, playlist_id: str) -> List[Track]:
        \"\"\"Descarga metadatos de TODAS las canciones (soporta 400+).\"\"\"
        if not self.api:
            raise ConnectionError('No autenticado')

        playlist_data = self.api.get_playlist(playlist_id, limit=None)
        tracks_data = playlist_data.get('tracks', [])
        
        clean_tracks = []
        for t in tracks_data:
            if not t.get('videoId'): 
                continue
                
            artists = ', '.join([a['name'] for a in t.get('artists', [])])
            album = t.get('album', {}).get('name', 'Unknown') if t.get('album') else 'Unknown'
            
            clean_tracks.append(Track(
                id=t['videoId'],
                title=t['title'],
                artist=artists,
                album=album,
                duration_seconds=t.get('duration_seconds', 0) or 0
            ))
        return clean_tracks

    def create_playlist(self, title: str, track_ids: List[str]):
        \"\"\"Crea una nueva playlist y añade canciones en lotes.\"\"\"
        if not self.api:
            raise ConnectionError('No autenticado')

        # 1. Crear Playlist vacía
        playlist_id = self.api.create_playlist(title, description='Ordenada con YTSorter')
        
        # 2. Añadir canciones (Lotes de 50)
        batch_size = 50
        for i in range(0, len(track_ids), batch_size):
            batch = track_ids[i:i + batch_size]
            self.api.add_playlist_items(playlist_id, batch)
            
        return playlist_id
