from spotipy import Spotify
from typing import List

class Track:
    def __init__(self):
        self.id: str
        self.name: str
        self.artist: str
        self.genre: str
        self.album: str
        self.cover: str

class Playlist:
    

    def __init__(self, url: str):
        self.tracklist: List[Track]
        self.url = url

    def populate(self, client: Spotify):
        offset = 0
        resposnse = client.playlist_items(
            self.url,
            offset=offset,
        )
