from spotify import SimilarSpotifyPlaylist
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, reources={r"/*": {"origins": "*"}})


@app.route('/connection', methods=['POST'])
def makePlaylist():
    data = request.get_json()

    spotify = SimilarSpotifyPlaylist(data['playlistLink'], 
                                     data['newPlaylistName'], 
                                     int(data['ratio']))
    
    return jsonify({"result": spotify.createNewPlaylist()})


if __name__ == '__main__':
    app.run(port=8080)