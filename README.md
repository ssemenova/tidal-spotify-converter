# Spotify -> Tidal batch upload

Batch upload your Spotify playlists into Tidal playlists, using [tidalapi](http://pythonhosted.org/tidalapi/_modules/tidalapi.html) and [spotipy](http://spotipy.readthedocs.io/).

## To run:

1. Clone this repository
2. Install the requirements: ```pip install -r requirements.txt```
3. Create a secrets.py file: ```touch secrets.py```
4. Copy and paste the following into the secrets file:
```
tidal_id = your_tidal_id
tidal_pwd = your_tidal_password
spotify_id = your_spotify_id
```
5. Run script.py: ```python script.py```

## To find your spotify ID
Go to your profile page on spotify, and click on the three dots > share > copy spotify URI. Then, when pasting the result into your secrets file, get rid of "spotify:user:" before the number.

## To find your tidal ID
Go to the tidal [web player](listen.tidal.com), click on your profile, copy the number in the url.
For example, mine looks like this: https://listen.tidal.com/profile/50530600, so I want 50530600
