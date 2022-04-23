from spotipy import Spotify
from typing import List, Dict

# Factory
# A single track i.e a single song
class Track:
    def __init__(self, name, artist, genre, cover, album):
        self.name = name
        self.artist = artist
        self.genre = genre
        self.cover = cover
        self.album = album

# Singleton
# A single playlist containing a list of tracks i.e songs
class Playlist:
    def __init__(self, url: str):
        self.tracklist: List[Track]
        self.url = url

    # Fill object with tracks using a client
    def populate(self, client: Spotify):
        offset = 0

        # Get response
        response = client.playlist_items(
            self.url,
            offset=offset,
            fields="items.track.id,total",
            additional_types=['track']
        )

        id_list = []
        track_id_list = []

        # ¯\_(ツ)_/¯
        if len(response['items']) != 0:
            offset = offset + len(response['items'])
        
        # Get track IDs for later use
        for element in id_list:
            track_id_list.append(element['track']['id'])

        # Populate the playlist structure with songs
        for element in track_id_list:
            uri = f'spotify:track:{element}'
            song_track = client.track(uri)
            artist_info = client.artist(song_track['artists'][0]['uri'])

            # Create new Track and append to self.tracklist
            self.tracklist.append(Track(
                song_track['name'],
                song_track['artists'][0]['name'],
                artist_info['genres'],
                song_track['album']['images'][0]['url'],
                song_track['album']['name']
            ))

    # Convert the Playlist to 4 separate lists of size of playlist size
    # This is a temporary method for compatibility with current codebase which requires 4 lists
    def getSeparateLists(self) -> Dict[str, List[str]]:
        song_name_list = []
        artist_list = []
        album_list = []
        cover_image_list = []
        for element in self.tracklist:
            song_name_list.append(element.name)
            artist_list.append(element.artist)
            cover_image_list.append(element.cover)
            album_list.append(element.album)
        return {
            'song_list' : song_name_list,
            'album_list' : album_list,
            'artist_list' : artist_list,
            'cover_images' : cover_image_list
        }
