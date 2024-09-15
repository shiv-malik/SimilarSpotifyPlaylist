import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        client_id="e757f266ee7f47f9a63820ce78414a81",
        client_secret="cd0aff901eb146df8ef1ca925c233051",
        # redirect_uri="https://localhost:5173",
        redirect_uri="https://google.com",
        scope="playlist-modify-public playlist-read-private"
    )
)

def getPlaylistID(link):
    return (link.split('playlist/')[1]).split('?si=')[0]


def getTracks(playlist, playlistLength, step=5):
    for offset in range(0, playlistLength, step):
        results = sp.playlist_tracks(playlist, limit=step, offset=offset)
        yield [track['track']['id'] for track in results['items']]


def getFeatures(tracks):
    return sp.audio_features(tracks)

def findSimilarTracks(tracks, ratio=1):
    features = getFeatures(tracks)
    dancability = sum([track['danceability'] for track in features]) / len(features)
    energy = sum([track['energy'] for track in features]) / len(features)

    recommendations = sp.recommendations(seed_tracks=tracks, 
                                         limit=int(ratio * len(tracks)),
                                         target_danceability=dancability,
                                         target_energy=energy)

    return [track['id'] for track in recommendations['tracks']]


if __name__ == '__main__':
    playlist = getPlaylistID('https://open.spotify.com/playlist/1Hs11dJy0ntKeUCOXVCvRx?si=827158cefeea40e3')
    
    sourceLength = sp.playlist_items(playlist, fields='total')['total']
    newPlaylistName = input('playlist name: ')
    ratio = int(input('ratio: '))
    # targetLength = 50
    # ratio = targetLength / sourceLength


    trackGenerator = getTracks(playlist, sourceLength)
    user = sp.current_user()['id']
    newPlaylist = sp.user_playlist_create(user=user, name=newPlaylistName, public=True)['id']

    while True:
        try:
            tracks = next(trackGenerator)
            similarTracks = findSimilarTracks(tracks, ratio)
            
            sp.playlist_add_items(playlist_id=newPlaylist, items=similarTracks)


        except StopIteration:
            break

    # tracks = getTracks(playlist)
    # similarTracks = findSimilarTracks(tracks, 25)

    
    # user_id = sp.current_user()['id']
    # new_playlist = sp.user_playlist_create(user=user_id, name='similarPlaylist', public=True)
    # new_playlist_id = new_playlist['id']

    # sp.playlist_add_items(playlist_id=new_playlist_id, items=similarTracks)