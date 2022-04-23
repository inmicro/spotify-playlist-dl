import os
import urllib.request
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import generalhf as ghf
import shutil

def getTrackData(uri, sp):
    all_music_data = {
        'song_name': "",
        'album_name': "",
        'artist_name': "",
        'cover_image': ""
    }
    song_track = sp.track(uri)
    all_music_data['song_list'] = song_track['name']
    # getting artist names
    all_music_data['artist_name'] = song_track['artists'][0]['name']
    all_music_data['album_name'] = song_track['album']['name']
    all_music_data['cover_image'] = song_track['album']['images'][0]['url']

    return all_music_data

def trackMetadataTagger(music_data):
    try:
        os.mkdir('album_art')
    except:
        pass
    outputdir = 'album_art\\'
    onlyfiles = [f for f in os.listdir('music/') if os.path.isfile(os.path.join('music/', f))]
    for file in onlyfiles:
        filepath = 'music/' + file
        audio = EasyID3(filepath)
        print('Getting album art for: ' + music_data['song_name'])
        urllib.request.urlretrieve(music_data['cover_image'], "album_art/image.jpg")
        print(music_data['cover_image'])
        audio['title'] = music_data['song_name']
        audio['artist'] = music_data['artist_name']
        audio['album'] = music_data['album_name']
        audio.save()
        audiox = ID3(filepath)
        with open('album_art/image.jpg', 'rb') as albumart:
            audiox['APIC'] = APIC(encoding=3, mime='image/jpg', type=3, desc='Cover', data=albumart.read())
            audiox.save()

def moveSong(song_name):
    new_folder_path = 'downloaded/tracks/'
    print(f'{ghf.bcolors.OKCYAN} Moving song to playlist dir {new_folder_path} {ghf.bcolors.ENDC}')
    try:
        os.mkdir(new_folder_path)
    except:
        pass
    file_names = os.listdir('music/')
    for file_name in file_names:
        shutil.move(os.path.join('music/', file_name), new_folder_path)