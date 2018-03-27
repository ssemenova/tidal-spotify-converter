from ..tidal-spotify-converter-secrets import tidal_id, tidal_username, tidal_pwd, spotify_id, spotify_username, spotify_discover_weekly_id, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import sys
import tidalapi


# Endpoints not in tidalapi
def get_tidal_create_playlist_url(tidal_id):
    return 'https://listen.tidal.com/v1/users/' + tidal_id + '/playlists'
def get_tidal_add_track_to_playlist_url(playlist_id):
    return 'https://listen.tidal.com/v1/playlists/' + playlist_id + '/items'
def get_tidal_find_track_url():
    return 'https://listen.tidal.com/v1/search/tracks'

# Endpoints not in spotipy
def get_discover_weekly_playlist():
    return 'https://api.spotify.com/v1/users/spotify/playlists/'  + spotify_discover_weekly_id + '/tracks'


def connect_to_spotify():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp, client_credentials_manager


def connect_to_tidal():
    tidal_session = tidalapi.Session()
    try:
        tidal_session.login(tidal_username, tidal_pwd)
    except requests.exceptions.HTTPError as e:
        print("Can't login to tidal for username=" + tidal_username + ", password=" + tidal_pwd)
        sys.exit()
    return tidal_session


def move_discover_weekly_from_spotify_to_tidal():
    try:
        r = requests.request(
           'GET',
           get_discover_weekly_playlist(),
           headers={
               'Authorization': 'Bearer ' + client_credentials_manager.get_access_token()
           }
        )
    except requests.exceptions.RequestException as e:
        print("Could not get Discovery Weekly playlist. Are you sure the ID is correct?")

    playlist = r.json()
    _add_playlist_to_tidal(playlist, tidal_session, playlist_name="Discover Weekly", tracks=playlist)


def _add_playlist_to_tidal(playlist, tidal_session, tracks=None, playlist_name=None):
    playlist_name_catch = playlist_name if playlist_name else playlist['name']
    playlist_id = _create_tidal_playlist(playlist_name_catch)

    if not playlist_id:
        return

    sanitized_tracks = []
    def _add_track_to_sanitized_list(tracks):
        for i, item in enumerate(tracks['items']):
            track = item['track']
            sanitized_tracks.append([
                track['name'], track['artists'][0]['name']
            ])

    tracks_catch = tracks if tracks else sp.user_playlist(spotify_id, playlist['id'], fields="tracks,next")['tracks']
    _add_track_to_sanitized_list(tracks)
    while tracks['next']:
        tracks = sp.next(tracks)
        _add_track_to_sanitized_list(tracks)

    _add_tracks_to_tidal_playlist(playlist_id, sanitized_tracks)


def _add_tracks_to_tidal_playlist(playlist_id, tracks):
    url = get_tidal_add_track_to_playlist_url(playlist_id)
    for name, artist in tracks:
        tidal_track_id = _search_for_track_on_tidal(name, artist)
        if tidal_track_id > -1:
            try:
                r = requests.request(
                    'POST',
                    url,
                    data={'trackIds':tidal_track_id, 'toIndex':1},
                    headers={
                        'x-tidal-sessionid': tidal_session.session_id,
                        'if-none-match': "*"
                    },
                    params={
                        'countryCode': 'US'
                    }
                )
            except requests.exceptions.RequestException as e:
                print('Error adding tracks to playlist: ' + e)
                # TODO: should add playlist name to CSV of failures


def _search_for_track_on_tidal(name, artist):
    id = -1;
    artist = artist.lower()

    def _artist_in_response(track):
        for response_artist in track['artists']:
            if response_artist['name'].lower() == artist:
                return True
        return False

    matched_artist = False
    offset = 0
    limit = 300
    end_of_track_list = False
    while not matched_artist and not end_of_track_list:
        try:
            r = requests.request(
                'GET',
                get_tidal_find_track_url(),
                headers={
                    'x-tidal-sessionid': tidal_session.session_id
                },
                params={
                    'offset': offset,
                    'countryCode': 'US',
                    'limit': limit,
                    'query': name
                }
            )

            if len(r.json()['items']) == 0:
                end_of_track_list = True

            for track in r.json()['items']:
                if _artist_in_response(track):
                    id = track['id']
                    matched_artist = True
                    break
            offset = offset + 300
            limit = offset + 300
        except requests.exceptions.RequestException as e:
            print('Could not make request for track name=' + name + ", artist=" + artist)
            # TODO: should add track name to CSV of failures

    if not matched_artist:
        print('Could not find track name=' + name + ", artist=" + artist)
        # TODO: should add track name to CSV of failures

    return id;


def _create_tidal_playlist(playlist_name):
    try:
        r = requests.request(
            'POST',
            get_tidal_create_playlist_url(tidal_id),
            data={'title':playlist_name, 'description':''},
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


def _add_tracks_to_spotify_playlist(track_ids, playlist_id):
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
    else:
        print "Can't get token for", username


sp, client_credentials_manager = connect_to_spotify()
tidal_session = connect_to_tidal()
move_discover_weekly_from_spotify_to_tidal()
