# Spotify -> Tidal batch upload

Batch upload your Spotify playlists into Tidal playlists, using [tidalapi](http://pythonhosted.org/tidalapi/_modules/tidalapi.html) and [spotipy](http://spotipy.readthedocs.io/).

Optionally, you can also run ```star_all_tracks_in_playlist``` with a Tidal playlist name to star all the songs in it, since there is no way to do that through the Tidal UI. I don't want to deal with Spotify authentification tbh so if you want to move all your songs from Spotify into Tidal, put them in a playlist, import that playlist using this script, then run star_all_tracks_in_playlist on that playlist. Then delete the playlist.

## To run:

1. Clone this repository
2. Install the requirements: ```pip install -r requirements.txt```
3. Create a secrets.py file: ```touch secrets.py```
4. Copy and paste the following into the secrets file. You want numbers for both the tidal and spotify IDs, not your email address.
```
tidal_id = 'your_tidal_id'
tidal_pwd = 'your_tidal_password'
spotify_id = 'your_spotify_id'
```
5. Run script.py: ```python script.py```
6. ???
7. Profit.
8. Any songs that could not be found on Tidal will be saved into a csv file called ```songs.csv```, along with the playlist they originally came from.

## To find your spotify ID
Go to your profile page on spotify, and click on the three dots > share > copy spotify URI. Then, when pasting the result into your secrets file, get rid of "spotify:user:" before the number.

## To find your tidal ID
Go to the tidal [web player](https://listen.tidal.com), click on your profile, copy the number in the url: https://listen.tidal.com/profile/thenumberyouwant.
