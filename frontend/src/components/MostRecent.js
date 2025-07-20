import React, {useState, useEffect} from 'react'

const MostRecent = ({selectedPlayer}) => {
    const [gameData, setGameData] = useState(null);

    const fetchMostRecentGameData = async () => {
        if (selectedPlayer) {
          const token = localStorage.getItem('access_token');
    
          try {
            const response = await fetch(`http://localhost:8000/api/player/recent_game_stats?player_name=${encodeURIComponent(selectedPlayer)}`, {
              headers: {
                  'Authorization': `Bearer ${token}`,
                  'Content-Type': 'application/json'
              }
            });
    
            const data = await response.json();
    
            if (response.ok) {
              const sanitizedData = {
                  player_name: selectedPlayer,
                  points: data["points"],
                  assists: data["assists"],
                  rebounds: data["rebounds"],
                  blocks: data["blocks"],
                  opponent: data["opponent"]
              };
              setGameData(sanitizedData);
            }
          } catch (err) {
            console.error('Error:', err);
          }
      }
    }

    useEffect(() => {
        fetchMostRecentGameData();

    }, [selectedPlayer])
  return (
    <div>
      <h2 style={{marginBottom: "20px"}}>Most Recent Game for {selectedPlayer} Analysis</h2>

      {gameData && 
            <table className="players-table">
              <thead>
                <tr>
                <th>Opponent</th>
                <th>Points</th>
            <th>Assists</th>
                <th>Rebounds</th>
                  <th>Blocks</th>
                </tr>
              </thead>
              <tbody>
                <tr>
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
  )
}

export default MostRecent;