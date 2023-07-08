import spotipy
import artistbridge
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os

SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_USER_ID = os.environ["SPOTIPY_USER_ID"]

scope = "playlist-modify-public"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri="http://example.com",
        scope=scope,
        open_browser=False,
        cache_path='cache.txt')
    )

new_playlist = sp.user_playlist_create(
    user=SPOTIPY_USER_ID, 
    name="cruel_summer_street_spirit", 
    public=True)



#search_results = sp.search("street spirit", type="track", limit=10)
#search_results = sp.search("cruel summer", type="track", limit=10)

#for i in search_results["tracks"]["items"]:
#    print(i["name"], i["id"])

starting_track = artistbridge.Track(song_id='1BxfuPKGuaTgP7aM0Bbdwr', sp=sp)
ending_track = artistbridge.Track(song_id="2QwObYJWyJTiozvs0RI7CF", sp=sp)

my_playlist = artistbridge.make_playlist(starting_track, ending_track, 50, sp=sp)

sp.user_playlist_add_tracks(
    SPOTIPY_USER_ID,
    playlist_id=new_playlist['uri'],
    tracks=[x.id for x in my_playlist]
)