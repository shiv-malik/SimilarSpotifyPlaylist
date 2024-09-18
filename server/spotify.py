import spotipy
from spotipy.oauth2 import SpotifyOAuth
from client_info import CLIENT_ID, CLIENT_SECRET

'''
Client info contains CLIENT_ID and CLIENT_SECRET which reference 
actual keys. Client info not included in git.
'''

sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="https://localhost:5173",
        scope="playlist-modify-public playlist-read-private"
    )
)


class SimilarSpotifyPlaylist:
    '''
    self._playlist: original playlist id.
    self._playlistLength: number of songs in original playlist (used with ratio to calculate
                          how many new songs to add to new playlist).
    self._newPlaylistName: name of new playlist to create.
    self._ratio: ratio of new songs to old songs (ie 1 means same number of songs, 2 means
                 double the number of songs in the new playlist, etc.).
    '''
    def __init__(self, playlistLink: str, newPlaylistName: str, ratio: int) -> None:
        self._playlist = (playlistLink.split('playlist/')[1]).split('?si=')[0]
        self._playlistLength = sp.playlist_items(self._playlist, fields='total')['total']
        self._newPlaylistName = newPlaylistName
        self._ratio = ratio

        self._newPlaylist = None

    @staticmethod
    def __getFeatures(tracks: list) -> list:
        '''
        Static function which returns features such as energy and dancability of 
        tracks passed in.
        '''
        return sp.audio_features(tracks)

    def __fetchTracks(self, step: int = 5):
        '''
        Generator function that returnns tracks in step increments. This is in the interest
        of saving memory and generating smaller batches of recommendations which can prevent
        over-generalization of songs and degrading effectiveness.
        '''
        for offset in range(0, self._playlistLength, step):
            results = sp.playlist_tracks(self._playlist, limit=step, offset=offset)
            yield [track['track']['id'] for track in results['items']]


    def __findSimilarTracks(self, tracks: list[5]) -> list:
        '''
        Searches through spotify's database and finds similar songs. The number 
        of songs to find is based on the ratio and the number of tracks passed in.
        '''
        features = SimilarSpotifyPlaylist.__getFeatures(tracks)
        dancability = sum([track['danceability'] for track in features]) / len(features)
        energy = sum([track['energy'] for track in features]) / len(features)
        recommendations = sp.recommendations(seed_tracks=tracks, 
                                            limit=int(self._ratio * len(tracks)),
                                            target_danceability=dancability,
                                            target_energy=energy)

        return [track['id'] for track in recommendations['tracks']]
    

    def __createPlaylistFrame(self) -> None:
        '''
        Creates new empty playlist that can be populated with songs. 
        Returns new playlist link.
        '''
        user = sp.current_user()['id']
        playlist = sp.user_playlist_create(user=user, name=self._newPlaylistName, public=True)
        self._newPlaylist = playlist['id']
        return playlist['external_urls']['spotify']

    def __addToPlaylist(self, tracks: list) -> None:
        '''
        Adds tracks to new playlist reference stored in class instance.
        '''
        sp.playlist_add_items(playlist_id=self._newPlaylist, items=tracks)

    
    def createNewPlaylist(self):
        '''
        Function that brings together the entire program. First creates playlist frame, then
        fetches tracks 5 at a time, finds similar tracks, and adds them to playlist.
        '''
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
    