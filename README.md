# artist-bridge

Example usage:
```{python}
import spotipy
from artistbridge import make_playlist

from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

scope = "playlist-modify-public"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri="http://example.com",
        scope=scope,
        open_browser=False)
    )

new_playlist = sp.user_playlist_create(
    user=SPOTIPY_USER_ID, 
    name="cruel_summer_street_spirit", 
    public=True)



#search_results = sp.search("street spirit", type="track", limit=10)
search_results = sp.search("cruel summer", type="track", limit=10)

for i in search_results["tracks"]["items"]:
    print(i["name"], i["id"])

starting_track = Track(song_id='1BxfuPKGuaTgP7aM0Bbdwr')
ending_track = Track(song_id="2QwObYJWyJTiozvs0RI7CF")

my_playlist = make_playlist(starting_track, ending_track, 50)

sp.user_playlist_add_tracks(
    SPOTIPY_USER_ID,
    playlist_id=new_playlist['uri'],
    tracks=[x.id for x in my_playlist]
)
```
