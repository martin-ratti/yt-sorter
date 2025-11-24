from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Track:
    id: str
    title: str
    artist: str
    album: str
    duration_seconds: int

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
    def sort_tracks(tracks: List[Track], criteria: str) -> List[Track]:
        # criteria puede ser: 'artist', 'title', 'album', 'duration'
        
        if criteria == 'duration':
            return sorted(tracks, key=lambda x: x.duration_seconds)
        
        if criteria == 'artist':
            # Orden secundario por título para consistencia
            return sorted(tracks, key=lambda x: (x.artist.lower(), x.title.lower()))
            
        if criteria == 'album':
            return sorted(tracks, key=lambda x: (x.album.lower(), x.artist.lower()))
            
        # Default: title
        return sorted(tracks, key=lambda x: x.title.lower())