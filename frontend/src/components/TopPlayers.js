import React, { useState } from 'react'

const TopPlayers = () => {
  const [selectedStat, setSelectedStat] = useState('')
  const [playersData, setPlayersData] = useState([])

  const fetchTop10Data = async (stat) => {
    if (stat) {
      const token = localStorage.getItem('access_token');

      fetch(`http://localhost:8000/api/player/top10?stat=${stat}`, {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
          setPlayersData(data)
        })
        .catch(error => {
          console.error('Error fetching top 10 data:', error)
          setPlayersData([])
        })
    } else {
      setPlayersData([])
    }
  }

  const handleStatChange = (e) => {
    const stat = e.target.value
    setSelectedStat(stat)
    
    if (stat) {
      fetchTop10Data(stat)
    }
  }

  return (
    <div>
      <h2 style={{marginBottom: "20px"}}>Top 10 Players</h2>
      
      <div className="dropdown-section">
        <label className="dropdown-label">
          <b>Show Top 10 Players By...</b>
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
            Top 10 Players by: <bold>{selectedStat.charAt(0).toUpperCase() + selectedStat.slice(1)}</bold>
          </p>
          
          {playersData && playersData.length > 0 ? (
            <table className="players-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Player Name</th>
                  <th>Total {selectedStat.charAt(0).toUpperCase() + selectedStat.slice(1)}</th>
                </tr>
              </thead>
              <tbody>
                {playersData.map((player, index) => (
                  <tr key={index}>
                    <td>{index + 1}</td>
                    <td>{player.player_name}</td>
                    <td>{player[`total_${selectedStat}`]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            selectedStat && <p>Sorry we couldn't find this data :/</p>
          )}
        </div>
      )}
    </div>
  )
}

export default TopPlayers;