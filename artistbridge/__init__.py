import spotipy
import numpy as np
from numpy.linalg import norm

class Track:
    def __init__(self, data=None, song_id=None, sp=None):
        self.sp = sp
        if song_id:
            data = sp.audio_features(tracks=[song_id,])[0]
        self.data = data
        self.id = data['id']
        self.vector = self.get_vector(data)

    def get_vector(self, data):
        song_vector = [
            data.get("danceability", 0),
            data.get("energy", 0),
            self.clip(data.get("loudness", 0), -60, 0, 60),
            data.get("speechiness", 0),
            data.get("acousticness", 0),
            data.get("instrumentalness", 0),
            data.get("liveness", 0),
            data.get("valence", 0),  # happiness
            self.clip(data.get("tempo", 0), 0, 200, 200),
        ]
        return np.array(song_vector)

    def clip(
        self,
        raw_value: int, 
        min_value: int, 
        max_value: int, 
        standardize: int = 0) -> float:
        """
        
        """
        clipped = max(min_value, min(max_value, raw_value))
        if min_value < 0:
            clipped += -min_value
        if standardize != 0:
            clipped /= standardize
        return clipped
    
    @staticmethod
    def cmp(left, right):
        """
        return the cosine similarity of the vector of two tracks
        """
        a, b = left.vector, right.vector
        cosine = np.dot(a,b) / (norm(a)*norm(b))
        return cosine

    def _recommendations(self):
        recs = self.sp.recommendations(
            seed_tracks=[self.id,]
        )

        return recs
    
    def recommendations(self):
        recs = self._recommendations()
        rec_ids = [r['id'] for r in recs['tracks']]
        return rec_ids

    def get_track(self):
        return self.sp.track(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)



def make_playlist(start_track: Track, end_track: Track, steps: int=10, sp=None):
    playlist_start = [start_track,]
    playlist_end = [end_track,]
    s = start_track
    e = end_track

    for i in range(steps//2):
        # get recommendations
        start_recs = [Track(song_id=x, sp=sp) for x in s.recommendations()]
        end_recs = [Track(song_id=x, sp=sp) for x in e.recommendations()]
        # make comparisons
        start_end_comparisons = [Track.cmp(s, x) for x in end_recs]
        end_start_comparisons = [Track.cmp(e, x) for x in start_recs]
        # pick the best
        s_index = np.argmax(end_start_comparisons)
        s = start_recs[s_index]
        e_index = np.argmax(start_end_comparisons)
        e = end_recs[e_index]
        playlist_start.append(s)
        playlist_end.append(e)

    full_playlist = playlist_start + playlist_end[::-1]
    sorted_playlist = sorted(set(full_playlist), key=lambda x: full_playlist.index(x))
    return sorted_playlist
