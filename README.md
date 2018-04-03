Minimal code required to run the move_discover_weekly_from_spotify_to_tidal function in a systemd job on my server. Uses client credentials workflow to automatically connect to spotify, instead of requiring a redirect uri.

The setup for this is specific to my server configuration, so YMMV with these steps. I use Arch Linux with systemd jobs, and already have python 3, pip, and virtualenv installed.

## Setup steps
1.  Clone https://github.com/ssemenova/tidal-spotify-converter.git onto your server
2.  Checkout the ```discover-weekly-systemd-job``` branch
2.  Create or copy ```secrets.py``` into the folder with the repository (see the master branch README for information about how to create the file)
3.  Create a virtual environment: ```virtualenv venv```
4.  Activate the virtual environment: ```sudo /venv/bin/activate```
5.  Install requirements: ```sudo pip install -r requirements.txt```
6.  Test that the script works: ```python script.py```
7.  Copy ```discover-weekly.timer``` and ```discover-weekly.service``` into ```/etc/systemd/system/``` (or wherever your systemd files are located)
8.  Copy ```discover_weekly.sh``` into ```/scripts/``` (or wherever you have bash scripts on your server)
9.  Reload daemons: ```sudo systemctl daemon-reload```
10.  Start the script: ```sudo systemctl start discover-weekly```

### discover-weekly.timer
```
[Unit]
Description=Discover Weekly Spotify -> Tidal Conversion

[Timer]
OnCalendar=weekly
RandomizedDelaySec=1h
Persistent=true

[Install]
WantedBy=timers.target
```

### discover-weekly.service
```
[Unit]
Description=DiscoverWeekly

[Service]
Type=oneshot
ExecStart=/bin/bash /scripts/discover_weekly.sh
```

### discover_weekly.sh
```
#!/bin/bash

cd /path/to/this/repository
source venv/bin/activate
python script.py
```

