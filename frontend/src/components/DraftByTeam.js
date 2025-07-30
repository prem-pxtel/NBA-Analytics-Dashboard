import React, { useState } from 'react';

const DraftByTeam = () => {
  const [teamName, setTeamName] = useState('');
  const [startYear, setStartYear] = useState('');
  const [endYear, setEndYear] = useState('');
  const [playersData, setPlayersData] = useState([]);
  const [error, setError] = useState('');

  const handleFetch = async () => {
    const token = localStorage.getItem('access_token');

    if (!teamName || !startYear || !endYear) {
      setError('Please fill in all fields.');
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/player/draft_by_team?team_name=${encodeURIComponent(teamName)}&start_year=${startYear}&end_year=${endYear}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch players');
      }

      const data = await response.json();
      setPlayersData(data);
      setError('');
    } catch (err) {
      console.error(err);
      setError('Failed to fetch players.');
      setPlayersData([]);
    }
  };

  return (
    <div>
      <h2 style={{ marginBottom: '20px' }}>Drafted Players by Team</h2>

      <div className="dropdown-section">
        <input
          type="text"
          placeholder="Team Name"
          value={teamName}
          onChange={(e) => setTeamName(e.target.value)}
          className="input"
        />
        <input
          type="text"
          placeholder="Start Year"
          value={startYear}
          onChange={(e) => setStartYear(e.target.value)}
          className="input"
        />
        <input
          type="text"
          placeholder="End Year"
          value={endYear}
          onChange={(e) => setEndYear(e.target.value)}
          className="input"
        />
        <button onClick={handleFetch} className="btn">Search</button>
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {playersData.length > 0 ? (
        <table className="players-table">
          <thead>
            <tr>
              <th>Player Name</th>
              <th>Draft Year</th>
              <th>Position</th>
              <th>Active</th>
            </tr>
          </thead>
          <tbody>
            {playersData.map((player, index) => (
              <tr key={index}>
                <td>{player.player_name}</td>
                <td>{player.draft_year}</td>
                <td>{player.position}</td>
                <td>{player.active_status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        !error && <p>Try searching something</p>
      )}
    </div>
  );
};

export default DraftByTeam;
