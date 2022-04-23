#! /usr/bin/python3

from typing import Tuple
import os
import urllib.request
from track import *
from youtube_search import YoutubeSearch
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from spotipy import Spotify
import yt_dlp
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import sys

# Setting the spotify credentials to access the web api
def setAuth(client_id: str, client_secret: str) -> Spotify:
    auth_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

# returns a dictionary with all the data about the music files
def getPlaylistTrackId(playlist_url, sp):

    # lists for IDs, track url, song names, etc
    id_list = []
    track_id_list = []
    song_name_list = []
    artist_list = []
    genre_list = []
    album_list = []
    cover_image_list = []
    offset = 0
    while True:
        response = sp.playlist_items(playlist_url,
                                     offset=offset,
                                     fields='items.track.id,total',
                                     additional_types=['track'])

        if len(response['items']) == 0:
            break
        offset = offset + len(response['items'])
        id_list = response['items']
    for element in id_list:
        track_id_list.append(element['track']['id'])

    for element in track_id_list:
        # getting song names
        uri = 'spotify:track:' + element
        song_track = sp.track(uri)
        song_name_list.append(song_track['name'])
        # getting artist names
        artist_list.append(song_track['artists'][0]['name'])
        album_list.append(song_track['album']['name'])
        artists_uri = song_track['artists'][0]['uri']
        artist_info = sp.artist(artists_uri)
        genre_list.append(artist_info['genres'])
        cover_image_list.append(song_track['album']['images'][0]['url'])

    return {
        'song_list' : song_name_list,
        'album_list' : album_list,
        'artist_list' : artist_list,
        'cover_images' : cover_image_list
    }

def getYoutubeIdfromSong(song_list, artist_list):
    result_list = []
    i = 0
    for _ in song_list:
        search_string = song_list[i] + ' ' + artist_list[i]
        results = YoutubeSearch(search_string, max_results=1).to_dict()
        print('got: ' + song_list[i] + ' by ' + artist_list[i])
        result_list.append(results)
        i+=1
    yt_id_list = createYoutubeIdList(result_list)
    return yt_id_list

def createYoutubeIdList(yt_results):
    ytIdList = []
    for elements in yt_results:
        for i in range(len(elements)):
            ytIdList.append(elements[i]['id'])
    return ytIdList

# Hook for showing download progress
def my_hook(d):
    if d['status'] == 'finished':
        print(f"-------{ d['filename'] } was finished downloading-------")
    elif d['status'] == 'downloading':
        print(f"Downloading {d['filename']}: {d['_percent_str']}% complete")

def downloadFromYtDL(id_list):
    url_list = []
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'progress_hooks': [my_hook],
        'outtmpl' : 'music/%(title)s.%(ext)s',
        'external_downloader_args': ['-loglevel', 'panic']
    }
    for id in id_list:
        url_list.append(('https://www.youtube.com/watch?v=' + id))
    for url in url_list:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def metadataTagger(music_data):
    try:
        os.mkdir('album_art')
    except:
        pass
    onlyfiles = [f for f in os.listdir('music/') if os.path.isfile(os.path.join('music/', f))]
    for file in onlyfiles:
        filepath = 'music/' + file
        audio = EasyID3(filepath)
        for i in range(len(music_data['song_list'])):
            if (music_data['song_list'][i]).lower() in file.lower():
                print('Getting album art for: ' + music_data['song_list'][i])
                urllib.request.urlretrieve(music_data['cover_images'][i], "album_art/image.jpg")
                print(music_data['cover_images'][i])
                audio['title'] = music_data['song_list'][i]
                audio['artist'] = music_data['artist_list'][i]
                audio['album'] = music_data['album_list'][i]
                audio.save()
                audiox = ID3(filepath)
                with open('album_art/image.jpg', 'rb') as albumart:
                    audiox['APIC'] = APIC(
                        encoding=3,
                        mime='image/jpg',
                        type=3, desc='Cover',
                        data=albumart.read()
                    )
                audiox.save()

def getCredentialsfromEnv() -> Tuple[str, str]:
    if "SPOTIFY_KEY" in os.environ and "SPOTIFY_SECRET" in os.environ:
        return (os.environ["SPOTIFY_KEY"], os.environ["SPOTIFY_SECRET"])
    else:
        client_id = input('Enter client ID: ')
        client_secret = input('Enter Client Secret: ')
        return (client_id, client_secret)


# Create Playlist
music_data = Playlist(sys.argv[1])

# Create client from credentials
creds = getCredentialsfromEnv()
client = setAuth(creds[0], creds[1])

# Populate the playlist with tracks using the client
music_data.populate(client)

# Convert to separate lists for now
lists = music_data.getSeparateLists()

# Get search results
yt_results = getYoutubeIdfromSong(lists['song_list'], lists['artist_list'])

# Donwload using the search results
downloadFromYtDL(yt_results)

# Attach metadata
metadataTagger(music_data)
