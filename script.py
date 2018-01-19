from secrets import tidal_id, tidal_username, tidal_pwd, spotify_id, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import sys
import tidalapi


# tidalapi does not have these endpoints
def get_tidal_create_playlist_url(tidal_id):
    return 'https://listen.tidal.com/v1/users/' + tidal_id + '/playlists'
def get_tidal_add_song_to_playlist_url(playlist_id):
    return 'https://listen.tidal.com/v1/playlists/' + playlist_id + '/items'
def get_tidal_find_song_url():
    return 'https://listen.tidal.com/v1/search/tracks'


def connect_to_spotify():
    scope = 'user-library-read'

    if len(sys.argv) > 1:
        spotify_username = sys.argv[1]
    else:
        print "Usage: %s username" % (sys.argv[0],)
        sys.exit()

    token = util.prompt_for_user_token(
        spotify_username,
        scope,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI
    )

    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get spotify token for " + username)
        sys.exit()

    return sp


def connect_to_tidal():
    tidal_session = tidalapi.Session()
    try:
        tidal_session.login(tidal_username, tidal_pwd)
    except requests.exceptions.HTTPError as e:
        print("Can't login to tidal for username=" + tidal_username + ", password=" + tidal_pwd)
        sys.exit()
    return tidal_session


def add_playlist_to_tidal(playlist, tidal_session):
    playlist_id = _create_playlist(playlist)

    if not playlist_id:
        return

    sanitized_tracks = []
    def _add_track_to_sanitized_list(tracks):
        for i, item in enumerate(tracks['items']):
            track = item['track']
            sanitized_tracks.append([
                track['name'], track['artists'][0]['name']
            ])

    tracks = sp.user_playlist(spotify_id, playlist['id'], fields="tracks,next")['tracks']
    _add_track_to_sanitized_list(tracks)
    while tracks['next']:
        tracks = sp.next(tracks)
        _add_track_to_sanitized_list(tracks)

    print("DEBUG: list of sanitized tracks: " + str(sanitized_tracks))
    _add_tracks_to_tidal_playlist(playlist_id, sanitized_tracks)


def _add_tracks_to_tidal_playlist(playlist_id, tracks):
    track_ids = []
    for name, artist in tracks:
        tidal_track_id = _search_for_track_on_tidal(name, artist)
        if tidal_track_id > -1:
            track_ids.append(tidal_track_id)

    print("DEBUG: list of track ids: " + str(track_ids))
    try:
        r = requests.request(
            'POST',
            get_tidal_add_song_to_playlist_url(playlist_id),
            data={'trackIds':track_ids[0], 'toIndex':1},
            headers={
                'x-tidal-sessionid': tidal_session.session_id,
                'if-none-match': '1'
            },
            params={
                'countryCode': 'US'
            }
        )

        # r = requests.request(
        #     'GET',
        #     'https://listen.tidal.com/playlist/' + playlist_id,
        #     headers={
        #         'x-tidal-sessionid': tidal_session.session_id,
        #     },
        #     params={
        #         'countryCode': 'US'
        #     }
        # )

    except requests.exceptions.RequestException as e:
        print('Error adding tracks to playlist: ' + e)
        # TODO: should add playlist name to CSV of failures


def _search_for_track_on_tidal(name, artist):
    id = -1;

    def _artist_in_response(track):
        for response_artist in track['artists']:
            if response_artist['name'] == artist:
                return True
        return False

    try:
        r = requests.request(
            'GET',
            get_tidal_find_song_url(),
            headers={
                'x-tidal-sessionid': tidal_session.session_id
            },
            params={
                'offset': 0,
                'countryCode': 'US',
                'limit': '50',
                'query': name
            }
        )

        matched_artist = False
        for track in r.json()['items']:
            if _artist_in_response:
                id = track['id']
                matched_artist = True;
                break;
    except requests.exceptions.RequestException as e:
        print('Could not make request for track name=' + name + ", artist=" + artist)
        # TODO: should add track name to CSV of failures

    if not matched_artist:
        print('Could not find track name=' + name + ", artist=" + artist)
        # TODO: should add track name to CSV of failures

    return id;


def _create_playlist(playlist):
    title = playlist['name']

    try:
        r = requests.request(
            'POST',
            get_tidal_create_playlist_url(tidal_id),
            data={'title':title, 'description':''},
            headers={
                'x-tidal-sessionid': tidal_session.session_id
            },
            params={
                'sessionId': tidal_session.session_id,
                'countryCode': 'US',
                'limit': '999'
            }
        )
    except requests.exceptions.RequestException as e:
        print('Error creating playlist: ' + e)
        # TODO: should add playlist name to CSV of failures
        return None

    return r.json()['uuid']


def favourite_track_in_tidal(track):
	pass


sp = connect_to_spotify()
tidal_session = connect_to_tidal()

# Get playlists
playlists = sp.user_playlists(spotify_id)
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("DEBUG: on playlist:" + playlist['name'])
        add_playlist_to_tidal(playlist, tidal_session)
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None

# Get user's saved tracks
saved_tracks = sp.current_user_saved_tracks()
for item in saved_tracks['items']:
    track = item['track']
    favourite_track_in_tidal(item)



# def _add_tracks_to_spotify_playlist():
#     if len(sys.argv) > 3:
#         username = sys.argv[1]
#         playlist_id = sys.argv[2]
#         track_ids = sys.argv[3:]
#     else:
#         print "Usage: %s username playlist_id track_id ..." % (sys.argv[0],)
#         sys.exit()
#
#     scope = 'playlist-modify-public'
#     token = util.prompt_for_user_token(username, scope)
#
#     if token:
#         sp = spotipy.Spotify(auth=token)
#         sp.trace = False
#         results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
#         print results
#     else:
#         print "Can't get token for", username
