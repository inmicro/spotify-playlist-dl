import os
import urllib.request
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import shutil
import generalhf as ghf
import time


# Playlist helper functions
def getPlaylistTrackId(playlist_url, sp):
    # lists for IDs, track url, song names, etc
    id_list = []
    track_id_list = []
    all_music_data = {
        'song_list': [],
        'album_list': [],
        'artist_list': [],
        'cover_images': []
    }
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
        all_music_data['song_list'].append(song_track['name'])
        # getting artist names
        all_music_data['artist_list'].append(song_track['artists'][0]['name'])
        all_music_data['album_list'].append(song_track['album']['name'])
        all_music_data['cover_images'].append(song_track['album']['images'][0]['url'])

    return all_music_data

def createYoutubeIdList(song_list, artist_list):
    id_list = []
    for i in range(len(song_list)):
        id_list.append(ghf.getYoutubeIdfromURL(song_list[i], artist_list[i]))
    return id_list

def downloadPlaylistTracks(id_list, quality):
    for id in id_list:
        ghf.downloadFromYtDL(id, quality)
    print(f'{ghf.bcolors.OKGREEN} Finished downloading all tracks {ghf.bcolors.ENDC}')


def playlistMetadataTagger(music_data):
    try:
        os.mkdir('album_art')
    except:
        pass
    outputdir = 'album_art\\'
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

def moveAllSongs(playlist_url, sp):
    playlist_name_path = ghf.getPlaylistName(playlist_url, sp) + '_' + time.strftime("%Y%m%d-%H%M%S") + '/'
    new_folder_path = 'downloaded/playlists/' + playlist_name_path
    print(f'{ghf.bcolors.OKCYAN} Moving all files to playlist dir {new_folder_path} {ghf.bcolors.ENDC}')
    try:
        os.mkdir(new_folder_path)
    except:
        pass
    file_names = os.listdir('music/')
    for file_name in file_names:
        shutil.move(os.path.join('music/', file_name), new_folder_path)
