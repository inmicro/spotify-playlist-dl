# spotify-playlist-dl
Mini python script to demonstrate how spotify can be cleverly worked around to get the songs in a playlist

## Instructions
1. Download the script and the requirements. You need to have Git installed.
```
git clone https://github.com/inmicro/spotify-playlist-dl
```
2. Get your spotify developer [api credentials](https://developer.spotify.com/dashboard/). Create a new application, put some info in it and then copy the Client ID and client secret
3. CD into the directory:
```
cd spotify-playlist-dl
```
4. Download the requirements
```
pip install -r requirements.txt
```
5. Run the script, with your first argument being the URL of the spotify playlist you want:
```
python3 main.py -m <mode> -u <spotify> URL
```
Check #flags to see all the available flags
6. It will ask for your credentials. Put them appropriately. Move the songs in the music directory away after the script has finished running.

7. You can create a file named ``creds`` and put in the client_id on the first line and client_secret on the second and it won't ask for creds each time

## Flags
```
-m / --mode <playlist/track> (REQUIRED)  -> Sets mode to playlist or track. For downloading individual track, set: -m track 
                                                                            for downloading playlist, set : -m playlist
-u / --url <URL of Playlist/Track>  (REQUIRED)    -> To set the URL of the playlist/track which you want to get.
-s / --storeformat <zip/folder> (OPTIONAL)  -> For playlists only. sets the format of how the final music should be stored, in a zipfile or in a folder. By default folder
-q / --quality <320k/128k/medium/insane> (Optional) -> Sets quality of ffmpeg encoded file. insane and 320k are the same thing. Same for 128k and medium. By default set to 192K
-h / --help Prints out detailed description of all flags and how to use them.
```

## Disclaimer
I do not condone piracy of any type. I personally buy all the music that I like from iTunes. This script is just for educational purposes(ie is a nice hack)

### Fork
Check out vaimer9's osm rewrite: https://github.com/Vaimer9/detach Try it out too! (The code is much nicer and easier to hack around)
#### Thanks
To the people who made spotipy, yt-dl and the contributors :)(Also the musicians)



