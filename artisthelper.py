import os
import urllib.request
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import shutil
import generalhf as ghf
import time


# Playlist helper functions
def getArtistTrackInfo(artist_url, number, sp):
    # lists for IDs, track url, song names, etc
    id_list = []
    track_id_list = []
    all_music_data = {
        'song_list': [],
        'album_list': [],
        'artist_list': [],
        'cover_images': []
    }

    results = sp.artist_top_tracks(artist_url)
    for track in results['tracks'][:number]:
        all_music_data['song_list'].append(track['name'])
        all_music_data['artist_list'].append(track['artists'][0]['name'])
        all_music_data['album_list'].append(track['album']['name'])
        all_music_data['cover_images'].append(track['album']['images'][0]['url'])

    return all_music_data
    
def artistZipUp(artist_name):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    zipfilename = artist_name + '_' + timestr
    shutil.make_archive(zipfilename, 'zip', 'music')
    shutil.rmtree('music/')
    shutil.rmtree('album_art/')

def artistMoveAllSongs(artist_name):
    artist_name_path = artist_name + '_' + time.strftime("%Y%m%d-%H%M%S") + '/'
    new_folder_path = 'downloaded/artists/' + artist_name_path
    print(f'{ghf.bcolors.OKCYAN} Moving all files to playlist dir {new_folder_path} {ghf.bcolors.ENDC}')
    try:
        os.mkdir(new_folder_path)
    except:
        pass
    file_names = os.listdir('music/')
    for file_name in file_names:
        shutil.move(os.path.join('music/', file_name), new_folder_path)




