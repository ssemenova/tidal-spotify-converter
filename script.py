from secrets import tidal_id, tidal_pwd, spotify_id
import tidalapi
import spotipy

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists(spotify_id)
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None

session = tidalapi.Session()
session.login(tidal_id, tidal_pwd)

favourites = tidalapi.Favorites(session, tidal_id)
print (favourites.tracks())


def star_all_tracks_in_playlist(playlist_name):
	pass


