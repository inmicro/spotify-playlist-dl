# spotify-playlist-dl
Mini python script to demonstrate how spotify can be cleverly worked around to get the songs in a playlist

## Instructions
- Download the script and the requirements. You need to have Git installed.
```
git clone https://github.com/inmicro/spotify-playlist-dl
```
- Get your spotify developer api credentials(https://developer.spotify.com/dashboard/). Create a new application, put some info in it and then copy the Client ID and client secret
- cd into the directory:
```
cd spotify-playlist-dl
```
- download the requirements
```
pip install -r requirements.txt
```
- Run the script, with your first argument being the URL of the spotify playlist you want:
```
python3 main.py <playlist url>
```
- It will ask for your credentials. Put them appropriately. Move the songs in the music directory away after the script has finished running.
- 
- You can create a file named ``creds`` and put in the client_id on the first line and client_secret on the second and it won't ask for creds each time


## Disclaimer
I do not condone piracy of any type. I personally buy all the music that I like from iTunes. This script is just for educational purposes(ie is a nice hack)
