from secrets import id, pwd
import tidalapi

session = tidalapi.Session()
session.login(id, pwd)

favourites = tidalapi.Favorites(session, username)
print (favourites.tracks())


