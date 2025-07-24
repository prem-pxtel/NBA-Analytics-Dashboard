import React, { useState, useEffect } from 'react'

const PlayerGameList = ({ selectedPlayer, onSelectGame }) => {
  const [gameData, setGameData] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('access_token');

    if (selectedPlayer) {
      fetch(`http://localhost:8000/api/player/game_stats?player_name=${encodeURIComponent(selectedPlayer)}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json())
        .then(data => {
          const sanitizedData = data.map(record => ({
            player_name: selectedPlayer,
            points: record["points"],
            assists: record["assists"],
            rebounds: record["rebounds"],
            blocks: record["blocks"],
            date: record["date"],
            opponent: record["opponent"]
          }));

          const sortedData = sanitizedData.sort((a, b) => {
            return new Date(b.date) - new Date(a.date);
          });

          setGameData(sortedData);
        });
    } else {
      setGameData([]);
    }
  }, [selectedPlayer])

  return (
    <div>
      {gameData.length != 0 ? (
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
            {gameData.map((game, index) => (
              <tr
                key={index}
                style={{ cursor: 'pointer' }}
                onClick={() => onSelectGame?.(game.game_id)}
              >
                <td>{game.date}</td>
                <td>{game.opponent}</td>
                <td>{game.points}</td>
                <td>{game.assists}</td>
                <td>{game.rebounds}</td>
                <td>{game.blocks}</td>
              </tr>
            ))}

          </tbody>
        </table>
      ) : <p>Sorry we couldn't find this game :/</p>}
    </div>
  )
}

export default PlayerGameList