import React, { useState } from 'react';
import { Link } from 'react-router-dom'
import axios from 'axios';
import './App.css';

function App() {
  const [playlistLink, setPlaylistLink] = useState('');
  const [newPlaylistName, setNewPlaylistName] = useState('');
  const [ratio, setRatio] = useState(1);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState(false);


  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!playlistLink || !newPlaylistName || ratio <= 0) {
      alert("Please fill in all fields correctly");
      return;
    }

    try {
      setLoading(true);
      setErr(false);
      setResult(false);
      const response = await axios.post('http://localhost:8080/connection', {
        playlistLink,
        newPlaylistName,
        ratio,
      });

      setResult(response.data.result);
      setLoading(false);
      console.log('New Playlist Created:', result);
    } 
    
    catch (error) {
      setLoading(false);
      setErr(true);
      console.error('Error creating playlist:', error);
    }
  };

  return (
    <div className="container">
      <h2>Create a Similar Spotify Playlist</h2>

      <form onSubmit={handleSubmit} className="form">
        <label>
          Source Playlist Link:
          <input
            type="text"
            value={playlistLink}
            onChange={(e) => setPlaylistLink(e.target.value)}
            placeholder="Enter Spotify Playlist Link"
            required
          />
        </label>

        <label>
          New Playlist Name:
          <input
            type="text"
            value={newPlaylistName}
            onChange={(e) => setNewPlaylistName(e.target.value)}
            placeholder="Enter New Playlist Name"
            required
          />
        </label>

        <label>
          Ratio of New to Old Songs:
          <input
            type="number"
            value={ratio}
            onChange={(e) => setRatio(e.target.value)}
            placeholder="Enter a Ratio (e.g., 1)"
            min="1"
            required
          />
        </label>

        {loading && (
          <button type="submit" className="submit-button" disabled={true}>Loading...</button>
        )}

        {!loading && (
          <button type="submit" className="submit-button">Create Playlist</button>
        )}
        
      </form>

      {result && !loading && !err && (
        <div>
          <h3>New Playlist Created!</h3>
          <p>{result.message}</p>
          <a href={result} target="_blank" rel="noopener noreferrer" className="playlist-link">
            Open Playlist
          </a>
        </div>
      )}
      
      {err && (
        <div>
          <h3 style={{color: 'red'}}>Error creating playlist.</h3>
          <h4 style={{color: 'red'}}>Please double-check link is correct.</h4>
        </div>
      )}

    </div>
  );
}

export default App;