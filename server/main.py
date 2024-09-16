from spotify import SimilarSpotifyPlaylist
from flask import Flask, request, jsonify
from flask_cors import CORS

if __name__ == '__main__':
    playlistLink = input('playlist link: ')
    newPlaylistName = input('new playlist name: ')
    ratio = int(input('ratio (new playlist length / old playlist length): '))

    spotify = SimilarSpotifyPlaylist(playlistLink, newPlaylistName, ratio)
    spotify.createNewPlaylist()