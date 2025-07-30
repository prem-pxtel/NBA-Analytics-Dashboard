import React, { useState, useEffect } from 'react'

const PlayerGameListByDate = ({selectedPlayer}) => {
  const [gameData, setGameData] = useState(null);
  const [selectedDate, setSelectedDate] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('access_token');

    if (selectedPlayer && selectedDate) {
      
      fetch(`http://localhost:8000/api/player/game_stats/by_date?player_name=${encodeURIComponent(selectedPlayer)}&date=${selectedDate}`, {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
      })
      .then(response => {
        return response.json();
      })
      .then(data => {
        const sanitizedData = {
          player_name: selectedPlayer,
          points: data["points"],
          assists: data["assists"],
          rebounds: data["rebounds"],
          blocks: data["blocks"],
          date: data["date"],
          opponent: data["opponent"]
        };
        
        setGameData(sanitizedData);
      })
    }
  }, [selectedPlayer, selectedDate]);

  const handleDateChange = (e) => {
    setSelectedDate(e.target.value);
  };

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <label>Select Date: </label>
        <input
          type="date"
          value={selectedDate}
          onChange={handleDateChange}
          placeholder="YYYY-MM-DD"
        />
      </div>

      {gameData && (
        <table className="players-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Opponent</th>
              <th>Points</th>
              <th>Assists</th>
              <th>Rebounds</th>
              <th>Blocks</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{gameData.date}</td>
              <td>{gameData.opponent}</td>
              <td>{gameData.points}</td>
              <td>{gameData.assists}</td>
              <td>{gameData.rebounds}</td>
              <td>{gameData.blocks}</td>
            </tr>
          </tbody>
        </table>
      )}

      {!gameData && selectedPlayer && selectedDate && (
        <p>No game found :/</p>
      )}
    </div>
  )
}

export default PlayerGameListByDate