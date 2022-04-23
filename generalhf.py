import os
import shutil
import time

import spotipy
import yt_dlp
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch


# COLORS
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Spotipy functions
# Getting authtoken from spotify
def setAuth(client_id, client_secret):
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

def getPlaylistName(playlist_id, sp):
    return sp.user_playlist(user=None, playlist_id=playlist_id, fields='name')['name']

# Youtube functions
def getYoutubeIdfromURL(song_name, artist_name):
    print(f'{bcolors.OKGREEN}Got youtube link for: {song_name} by {artist_name}{bcolors.ENDC}')
    search_string = song_name + ' ' + artist_name
    results = YoutubeSearch(search_string, max_results=1).to_dict()
    return results[0]['id']

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def downloadFromYtDL(id, quality):
    if quality == '320k' or quality == 'insane':
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'progress_hooks': [my_hook],
            'outtmpl': 'music/%(title)s.%(ext)s',
        }
    elif quality == '128k' or quality == 'average':
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
            'progress_hooks': [my_hook],
            'outtmpl': 'music/%(title)s.%(ext)s',
        }
    else:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [my_hook],
            'outtmpl': 'music/%(title)s.%(ext)s',
        }
    url = 'https://www.youtube.com/watch?v=' + id
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

# General/User functions

def authTokenset():
    if os.path.isfile('creds'):
        with open('creds') as file:
            lines = [line.rstrip() for line in file]
        authtoken = setAuth(lines[0], lines[1])
    else:
        while True:
            print(f'{bcolors.OKBLUE}Enter client ID: {bcolors.ENDC}')
            client_id = input()
            print(f'{bcolors.OKBLUE}Enter Client Secret: {bcolors.ENDC}')
            client_secret = input()
            try:
                authtoken = setAuth(client_id, client_secret)
                print(f'{bcolors.OKCYAN}Set spotify credentials.{bcolors.ENDC}')
                print(f'btw... you can set and forget your creds in a creds file')
                break
            except:
                # TODO Get better exceptions
                print(f'{bcolors.WARNING} COULD NOT SET CREDENTIALS: PLEASE CHECK YOUR CREDENTIALS{bcolors.ENDC}')
    return authtoken

def zipItUp(playlist_id, sp):
    results = sp.user_playlist(user=None, playlist_id=playlist_id, fields="name")
    timestr = time.strftime("%Y%m%d-%H%M%S")
    zipfilename = results['name'] + '_' + timestr
    shutil.make_archive(zipfilename, 'zip', 'music')
    shutil.rmtree('music/')
    shutil.rmtree('album_art/')

