import React, { useState } from 'react';

const EditStatsForm = ({ selectedPlayer }) => {
  const [gameId, setGameId] = useState('');
  const [formData, setFormData] = useState({
    points: '',
    assists: '',
    rebounds: '',
    blocks: '',
    FGA: '',
    FGM: '',
    FTA: '',
    FTM: '',
  });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem('access_token');
    if (!token) return setMessage('User not logged in.');

    const body = {
      player_name: selectedPlayer,
      game_id: gameId,
      ...Object.fromEntries(
        Object.entries(formData).filter(([_, v]) => v !== '')
      )
    };


    try {
      const response = await fetch('http://localhost:8000/api/player/update_game_stats', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(body)
      });

      const result = await response.json();
      if (response.ok) {
        setMessage('Stats updated successfully!');
      } else {
        console.error(result);
        setMessage(result.error || 'Update failed. You may not be an admin.');
      }
    } catch (err) {
      console.error(err);
      setMessage('Something went wrong.');
    }
  };

  return (
    <div style={{ marginTop: '30px', padding: '10px', border: '1px solid #ccc', maxWidth: '400px' }}>
      <h3>Edit Stats for: {selectedPlayer}</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Game ID"
          value={gameId}
          onChange={(e) => setGameId(e.target.value)}
          required
        />
        {["points", "assists", "rebounds", "blocks", "FGA", "FGM", "FTA", "FTM"].map((field) => (
          <input
            key={field}
            type="number"
            name={field}
            placeholder={field}
            value={formData[field]}
            onChange={handleChange}
            style={{ display: 'block', margin: '5px 0' }}
          />
        ))}
        <button type="submit">Update Stats</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default EditStatsForm;
