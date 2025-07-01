import React, {useState, useEffect} from 'react'

const PlayersList = ({searchTerm}) => {
    const [playersData, setPlayersData] = useState([]);

    useEffect(() => {
        if (searchTerm) {
            console.log("Ok we searching player with name =", searchTerm)
            fetch(`http://localhost:8000/api/player/player_stats?player_name=${encodeURIComponent(searchTerm)}`)
                .then(response => response.json())
                .then(data => {
        const santizedData = data.season_stats.map(record => ({
            player_name: record[0],
            year: record[1],
                        team_name: record[2],
            points_per_game: record[3],
            assists_per_game: record[4],
            rebounds_per_game: record[5],
            blocks_per_game: record[6]
        }));
        setPlayersData(santizedData);
                });
        } else {
            setPlayersData([]);
        }
    }, [searchTerm])

    return (
        <div>
            {playersData.length != 0 ? (
            <table className="players-table">
                <thead>
                    <tr>
                        <th>Player</th>
                        <th>Season</th>
                            <th>Team</th>
                                  <th>Points per game</th>
                            <th>Assists per game</th>
                <th>Rebounds per game</th>
                <th>Blocks per game</th>
            </tr>
        </thead>
        <tbody>
            {playersData.map((playerSeason, index) => (
                <tr key={index}>
                        <td>{playerSeason.player_name}</td>
                    <td>{playerSeason.year}</td>
                <td>{playerSeason.team_name}</td>
                            <td>{playerSeason.points_per_game}</td>
                            <td>{playerSeason.assists_per_game}</td>
                                      <td>{playerSeason.rebounds_per_game}</td>
                            <td>{playerSeason.blocks_per_game}</td>
                        </tr>
                        ))}
                    </tbody>
                </table>
            ) : <p>We couldn't find any players by that name : /</p>}
        </div>
    )
}

export default PlayersList;