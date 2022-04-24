import argparse

import generalhf as ghf
import playlisthelper as phf
import trackhelper as thf
import artisthelper as ahf

parser = argparse.ArgumentParser(description='Download spotify playlists')
parser.add_argument('-m', '--mode', help='Set mode to playlist or track or artist', required=True)
parser.add_argument('-u', '--url', help='spotify URL', required=True)
parser.add_argument('-s', '--storeformat', help='Zip it or put it in a folder', required=False, default='folder')
parser.add_argument('-q', '--quality', help='320k(or insane) or 128k(or medium) or 192k', required=False, default='128k')
parser.add_argument('-n', '--number', help='Number of top songs. Relevant for artist switch', required=False, default='5')

args = vars(parser.parse_args())


def playlist_flow(playlist_id, storeformat):
    print(f'{ghf.bcolors.OKBLUE}setting authtoken{ghf.bcolors.ENDC}')
    authToken = ghf.authTokenset()
    print(f'{ghf.bcolors.OKBLUE}getting names of spotify tracks{ghf.bcolors.ENDC}')
    music_data = phf.getPlaylistTrackInfo(playlist_id, authToken)
    print(f'{ghf.bcolors.OKBLUE}Searching youtube for the songs{ghf.bcolors.ENDC}')
    yt_results = phf.createYoutubeIdList(music_data['song_list'], music_data['artist_list'])
    print(f'{ghf.bcolors.OKBLUE}now downloading{ghf.bcolors.ENDC}')
    phf.downloadPlaylistTracks(yt_results, args['quality'])
    print(f'{ghf.bcolors.ENDC}setting metadata{ghf.bcolors.ENDC}')
    phf.playlistMetadataTagger(music_data)
    if storeformat == 'folder':
        phf.moveAllSongs(playlist_id, authToken)
    elif storeformat == 'zip':
        ghf.zipItUp(playlist_id, authToken)
    else:
        print(f'{ghf.bcolors.WARNING} Invalid storeformat option chosen. Please choose between zip or folder. Defaulting to folder for now.{ghf.bcolors.ENDC}')
        phf.moveAllSongs(playlist_id, authToken)
        


def trackFlow(track_url, quality):
    print(f'{ghf.bcolors.OKBLUE}setting authtoken{ghf.bcolors.ENDC}')
    authToken = ghf.authTokenset()
    print(f'{ghf.bcolors.OKBLUE}getting info about track{ghf.bcolors.ENDC}')
    track_info = thf.getTrackData(track_url, authToken)
    print(f'{ghf.bcolors.OKBLUE}Searching youtube for the song{ghf.bcolors.ENDC}')
    song_yt_id = ghf.getYoutubeIdfromURL(track_info['song_name'], track_info['artist_name'])
    ghf.downloadFromYtDL(song_yt_id, quality)
    thf.trackMetadataTagger(track_info)
    thf.moveSong(track_info['song_name'])

def artistTrackFlow(url, n, storeformat):
    print(f'{ghf.bcolors.OKBLUE}setting authtoken{ghf.bcolors.ENDC}')
    authToken = ghf.authTokenset()
    print(f'{ghf.bcolors.OKBLUE}getting names of top  tracks{ghf.bcolors.ENDC}')
    music_data = ahf.getArtistTrackInfo(url, n, authToken)
    print(f'{ghf.bcolors.OKBLUE}Searching youtube for the songs{ghf.bcolors.ENDC}')
    yt_results = phf.createYoutubeIdList(music_data['song_list'], music_data['artist_list'])
    print(f'{ghf.bcolors.OKBLUE}now downloading{ghf.bcolors.ENDC}')
    phf.downloadPlaylistTracks(yt_results, args['quality'])
    print(f'{ghf.bcolors.ENDC}setting metadata{ghf.bcolors.ENDC}')
    phf.playlistMetadataTagger(music_data)
    if storeformat == 'folder':
        ahf.artistMoveAllSongs(music_data['artist_list'][0])
    elif storeformat == 'zip':
        ahf.artistZipUp(music_data['artist_list'][0])
    else:
        print(f'{ghf.bcolors.WARNING} Invalid storeformat option chosen. Please choose between zip or folder. Defaulting to folder for now.{ghf.bcolors.ENDC}')
        ahf.artistMoveAllSongs(music_data['artist_list'][0])
        
if (args['mode'] == 'playlist') and (len(args['url']) > 10) and (args['storeformat'] == 'zip' or args['storeformat'] == 'folder'):
    playlist_flow(args['url'], args['storeformat'])
elif (args['mode'] == 'track') and (len(args['url']) > 10):
    trackFlow(args['url'], args['quality'])
elif (args['mode'] == 'artist') and (len(args['url']) > 10) and (args['storeformat'] == 'zip' or args['storeformat'] == 'folder'):
    artistTrackFlow(args['url'], int(args['number']), args['storeformat'])
else:
    print(f'{ghf.bcolors.WARNING} Invalid mode or URL passed. Use -h for more help {ghf.bcolors.ENDC}')
