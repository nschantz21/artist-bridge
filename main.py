from flask import Flask, render_template, request, url_for, redirect
import artistbridge
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os
from typing import Union

SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_USER_ID = os.environ["SPOTIPY_USER_ID"]

scope = "playlist-modify-public"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                              client_secret=SPOTIPY_CLIENT_SECRET,
                              redirect_uri="http://example.com",
                              scope=scope,
                              open_browser=False,
                              cache_path='cache.txt'))


def playlist_create(song1: str, song2: str, name: str) -> str:
    new_playlist = sp.user_playlist_create(user=SPOTIPY_USER_ID,
                                           name=name,
                                           public=True)
    starting_track = artistbridge.Track(song_id=song1, sp=sp)
    ending_track = artistbridge.Track(song_id=song2, sp=sp)
    my_playlist = artistbridge.make_playlist(starting_track,
                                             ending_track,
                                             10,
                                             sp=sp)
    sp.user_playlist_add_tracks(SPOTIPY_USER_ID,
                                playlist_id=new_playlist['uri'],
                                tracks=[x.id for x in my_playlist])
    url = f"https://open.spotify.com/embed/playlist/{new_playlist['uri'].split(':')[-1]}?utm_source=generator"
    return url


# Create a flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

messages = []


@app.route('/')
def index():
    return render_template('index.html', messages=messages)


# Index page
@app.route('/create/', methods=("GET", "POST"))
def create():

    if request.method == "POST":
        song1 = request.form['song1']
        song2 = request.form['song2']
        name = request.form['name']
        if not song1:
            #flash('title is required!')
            pass
        elif not song2:
            #flash('Content is required!')
            pass
        elif not name:
            pass
        else:
            playlist_url = playlist_create(song1, song2, name)
            messages.append({
                'song1': song1,
                'song2': song2,
                'playlist_url': playlist_url
            })
            return redirect(url_for('index'))

    return render_template('create.html')


if __name__ == ' __main__':
    # Run the Flask app
    app.run(host='0.0.0.0', debug=True, port=8080)
