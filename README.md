# Spotify -> Tidal batch upload

A suite of helpful (to me) functions to transfer data from Spotify to Tidal, and vice versa, using [tidalapi](http://pythonhosted.org/tidalapi/_modules/tidalapi.html) and [spotipy](http://spotipy.readthedocs.io/). Because Tidal does not have a public-facing API, if they change their URLs or requirements, this will break. Feel free to submit a bug report if it does and I'll try to fix it if I can.

## Things you can do

### delete_all_tidal_playlists()
Delete all your tidal playlists.

### move_all_tidal_playlists_to_spotify()
Move all your tidal playlists to spotify.

### move_one_tidal_playlist_to_spotify(playlist_id)
Move one of your tidal playlists to spotify. Takes a playlist ID

### move_all_spotify_playlists_to_tidal()
Move all of your spotify playlists to tidal.

### move_favourites_from_spotify_to_tidal()
Move all your favourites/liked/saved tracks from spotify to your favourites tracks in tidal.

### move_discover_weekly_from_spotify_to_tidal()
Move a discovery weekly playlist on spotify to tidal. A minimal version of this repository that calls this function and is configured to run on my server is in [this branch](https://github.com/ssemenova/tidal-spotify-converter/tree/discover-weekly-systemd-job).

There are also ```connect_to_spotify``` and ```connect_to_tidal``` functions, which you must run before running any of the other functions. Both authenticate you and return either a spotipy or tidalapi session.


## To run

1. Clone this repository
2. Install the requirements: ```pip install -r requirements.txt```
3. Create a secrets.py file: ```touch secrets.py```
4. Copy and paste the following into the secrets file. You want numbers for both the tidal and spotify IDs, not your email address. See the sections below for how to obtain both your tidal and spotify IDs, as well as spotify client credentials.
```
tidal_id = 'your_tidal_id'
tidal_pwd = 'your_tidal_password'
spotify_id = 'your_spotify_id'
tidal_username = 'your_tidal_email_address@email.com'
spotify_username = 'your_spotify_email_address@email.com'
SPOTIPY_CLIENT_ID = 'your_spotify_client_ID'
SPOTIPY_CLIENT_SECRET = 'your_spotify_client_secret'
SPOTIPY_REDIRECT_URI = 'http://localhost/'
spotify_discover_weekly_id = 'your_spotify_discover_weekly_id'
```
5. Run script.py: ```python script.py```. Right now, the script just signs into Spotify, signs into Tidal, and moves all Spotify songs to Tidal, but you can edit the script to run whatever functions you want.
6. ???
7. Profit.

## To find your spotify ID
Go to your profile page on spotify, and click on the three dots > share > copy spotify URI. Then, when pasting the result into your secrets file, get rid of "spotify:user:" before the number.

## To find your tidal ID
Go to the tidal [web player](https://listen.tidal.com), click on your profile, copy the number in the url: https://listen.tidal.com/profile/thenumberyouwant.

## To find your spotify discover weekly ID
Go to your discover weekly playlist on spotify, and click on the three dots > share > copy playlist link. Then, when pasting the results into your secret file, copy the number between "https://open.spotify.com/user/spotify/playlist/" and "?si=bunchOfRandomThings".

## Get spotify API client credentials
For some reason, there is no Spotify how-to on this that I can find, so here it is:
1. Go [here](https://beta.developer.spotify.com/dashboard/), sign in with your spotify account, and register an app.
2. Click on the app, and copy the client ID and client secret into your secrets file.
3. Click 'edit settings' in the top right corner.
4. Scroll down to 'Redirect URIs' and add 'http://localhost/'
5. Save
Now you should be able to log in when running the program. A window will pop up asking you to sign in, and then the program will continue running.

## Does it work?
Eh, good enough. A lot of songs aren't found because of the discrepancies between the two platforms with song names and artist names (Admiral vs. The Admiral). Further, a lot of songs have addendums - "We Belong - Odesza Remix", or "Storm Returns (A Prefuse/Tommy Guerrero Interlude)". A more dedicated programmer might parse the song names, perhaps getting rid of anything after a dash or anything between parenthesis. But this doesn't work all the time (I want the Odesza remix of We Belong, not the original!). The Tidal library is also a lot smaller than the Spotify library, unfortunately. If you would like to submit a PR to make this part of the code more robust, I would greatly welcome it.
