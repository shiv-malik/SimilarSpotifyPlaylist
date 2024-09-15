from spotify import sp, getPlaylistID, getTracks, findSimilarTracks

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