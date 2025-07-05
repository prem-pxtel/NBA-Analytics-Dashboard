import React, { useState } from 'react'

const BestGame = ({selectedPlayer}) => {
  const [selectedStat, setSelectedStat] = useState('')
  const [gameData, setGameData] = useState({});


  const fetchBestGameData = async (stat) => {
    if (stat && selectedPlayer) {
        fetch(`http://localhost:8000/api/player/game_stats/by_stat?player_name=${encodeURIComponent(selectedPlayer)}&stat=${stat}`)
            .then(response => response.json())
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
    });
    } else {
        setGameData({});
    }
  }

  const handleStatChange = (e) => {
    const stat = e.target.value
    setSelectedStat(stat)
    
    if (stat) {
      fetchBestGameData(stat)
    }
  }

  return (
    <div>
      <h2 style={{marginBottom: "20px"}}>Best Game Analysis</h2>
      
      <div className="dropdown-section">
        <label className="dropdown-label">
          <b>Show Best Game For {selectedPlayer} By...</b>
        </label>
        <br />
        <br />

        
        <select
          id="stat-select"
          value={selectedStat}
          onChange={handleStatChange}
          className="stat-select"
        >
          <option value="">Select a statistic...</option>
          <option value="points">Points</option>
            <option value="rebounds">Rebounds</option>
            <option value="assists">Assists</option>
            <option value="blocks">Blocks</option>
        </select>
      </div>

      {selectedStat && (
        <div>
          <p>
            You selected: <bold>{selectedStat.charAt(0).toUpperCase() + selectedStat.slice(1)}</bold>
          </p>
          
          {gameData && 
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
          }
        </div>
      )}
    </div>
  )
}

export default BestGame