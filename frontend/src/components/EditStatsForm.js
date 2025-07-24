import React, { useState } from 'react';

function EditStatsForm({ selectedPlayer }) {
  const [gameId, setGameId] = useState('');
  const [points, setPoints] = useState('');
  const [assists, setAssists] = useState('');
  const [rebounds, setRebounds] = useState('');
  const [blocks, setBlocks] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState('');

  console.log("HELOOO")

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setMessage('');


    try {
      const token = localStorage.getItem('access_token');

      const res = await fetch('http://localhost:8000/api/player/update_game_stats', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          player_name: selectedPlayer,
          game_id: gameId,
          points: points ? parseInt(points) : null,
          assists: assists ? parseInt(assists) : null,
          rebounds: rebounds ? parseInt(rebounds) : null,
          blocks: blocks ? parseInt(blocks) : null,
        }),
      });

      if (!res.ok) {
        throw new Error(`Status: ${res.status}`);
      }

      const data = await res.json();
      console.log('Update successful:', data);
      setMessage('Player stats updated successfully.');

    } catch (err) {
      console.warn('User is likely not an admin or update failed silently.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div style={{ marginTop: '20px' }}>
      HIII
      <h2>Edit Player Stats (Admin Only)</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Game ID"
          value={gameId}
          onChange={(e) => setGameId(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Points"
          value={points}
          onChange={(e) => setPoints(e.target.value)}
        />
        <input
          type="number"
          placeholder="Assists"
          value={assists}
          onChange={(e) => setAssists(e.target.value)}
        />
        <input
          type="number"
          placeholder="Rebounds"
          value={rebounds}
          onChange={(e) => setRebounds(e.target.value)}
        />
        <input
          type="number"
          placeholder="Blocks"
          value={blocks}
          onChange={(e) => setBlocks(e.target.value)}
        />
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Submitting...' : 'Submit'}
        </button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default EditStatsForm;
