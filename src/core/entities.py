from dataclasses import dataclass
from typing import List
import random
import unicodedata

@dataclass
class Track:
    id: str
    title: str
    artist: str
    album: str
    duration_seconds: int
    original_index: int = 0

    def to_dict(self):
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "duration": self.duration_seconds
        }

class PlaylistSorter:
    """Lógica pura de ordenamiento."""
    
    @staticmethod
    def _normalize(text: str) -> str:
        """Convierte 'Árbol' en 'arbol' para ordenar correctamente."""
        if not text: return ""
        # Normaliza caracteres unicode (separa la tilde de la letra)
        nfkd_form = unicodedata.normalize('NFKD', text)
        # Se queda solo con las letras base (elimina marcas diacríticas) y pasa a minúsculas
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

    @staticmethod
    def sort_tracks(tracks: List[Track], criteria: str, reverse: bool = False) -> List[Track]:
        result = []
        
        if criteria == 'shuffle':
            result = tracks.copy()
            random.shuffle(result)
        elif criteria == 'duration':
            result = sorted(tracks, key=lambda x: x.duration_seconds)
        elif criteria == 'artist':
            # Ordenamos usando la versión normalizada (sin acentos)
            result = sorted(tracks, key=lambda x: (
                PlaylistSorter._normalize(x.artist), 
                PlaylistSorter._normalize(x.title)
            ))
        elif criteria == 'album':
            result = sorted(tracks, key=lambda x: (
                PlaylistSorter._normalize(x.album), 
                PlaylistSorter._normalize(x.artist)
            ))
        else: # Default: title
            result = sorted(tracks, key=lambda x: PlaylistSorter._normalize(x.title))
            
        if reverse and criteria != 'shuffle':
            result.reverse()
            
        return result