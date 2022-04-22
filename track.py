from spotipy import Spotify
from typing import List

class Track:
    def __init__(self, name, artist, genre, cover):
        self.name = name
        self.artist = artist
        self.genre = genre
        self.cover = cover

class Playlist:
    def __init__(self, url: str):
        self.tracklist: List[Track]
        self.url = url

    def populate(self, client: Spotify):
        offset = 0
        response = client.playlist_items(
            self.url,
            offset=offset,
            fields="items.track.id,total",
            additional_types=['track']
        )

        id_list = []
        track_id_list = []
        if len(response['items']) != 0:
            offset = offset + len(response['items'])
        
        for element in id_list:
            track_id_list.append(element['track']['id'])

        for element in track_id_list:
            uri = f'spotify:track:{element}'
            song_track = client.track(uri)
            artist_info = client.artist(song_track['artists'][0]['uri'])
            self.tracklist.append(Track(
                song_track['name'],
                song_track['artists'][0]['name'],
                artist_info['genres'],
                song_track['album']['images'][0]['url']

            ))
