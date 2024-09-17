import spotipy
from spotipy.oauth2 import SpotifyOAuth
from client_info import CLIENT_ID, CLIENT_SECRET

sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        # redirect_uri="https://localhost:5173",
        redirect_uri="https://google.com",
        scope="playlist-modify-public playlist-read-private"
    )
)

class SimilarSpotifyPlaylist:

    def __init__(self, playlistLink, newPlaylistName, ratio):
        self._playlist = (playlistLink.split('playlist/')[1]).split('?si=')[0]
        self._playlistLength = sp.playlist_items(self._playlist, fields='total')['total']
        self._newPlaylistName = newPlaylistName
        self._ratio = ratio

        self._newPlaylist = None

    @staticmethod
    def __getFeatures(tracks: list) -> list:
        return sp.audio_features(tracks)

    def __fetchTracks(self, step: int = 5):  #fetches tracks in step increments at a time
        for offset in range(0, self._playlistLength, step):
            results = sp.playlist_tracks(self._playlist, limit=step, offset=offset)
            yield [track['track']['id'] for track in results['items']]

    def __findSimilarTracks(self, tracks: list[5]):
        features = SimilarSpotifyPlaylist.__getFeatures(tracks)
        dancability = sum([track['danceability'] for track in features]) / len(features)
        energy = sum([track['energy'] for track in features]) / len(features)
        recommendations = sp.recommendations(seed_tracks=tracks, 
                                            limit=int(self._ratio * len(tracks)),
                                            target_danceability=dancability,
                                            target_energy=energy)

        return [track['id'] for track in recommendations['tracks']]
    

    def __createPlaylistFrame(self):
        user = sp.current_user()['id']
        playlist = sp.user_playlist_create(user=user, name=self._newPlaylistName, public=True)
        self._newPlaylist = playlist['id']
        return playlist['external_urls']['spotify']

    def __addToPlaylist(self, tracks: list):
        sp.playlist_add_items(playlist_id=self._newPlaylist, items=tracks)

    
    def createNewPlaylist(self):
        trackGenerator = self.__fetchTracks()
        newPlaylistLink = self.__createPlaylistFrame()
        while True:
            try:
                tracks = next(trackGenerator)
                similarTracks = self.__findSimilarTracks(tracks)
                self.__addToPlaylist(similarTracks)
            except StopIteration:
                break
        
        return newPlaylistLink