import React, {useState, useEffect} from 'react'

const PlayersList = ({searchTerm, handleSelectPlayer}) => {
    const [playersData, setPlayersData] = useState([]);

    useEffect(() => {
        if (searchTerm) {
            fetch(`http://localhost:8000/api/player/season_stats?player_name=${encodeURIComponent(searchTerm)}`)
                .then(response => response.json())
                .then(data => {
        const santizedData = data.map(record => ({
            player_name: record["player_name"],
            year: record["season_id"],
                        team_name: record["team_name"],
            points_per_game: record["points_per_game"],
            assists_per_game: record["assists_per_game"],
            rebounds_per_game: record["rebounds_per_game"],
            blocks_per_game: record["blocks_per_game"]

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
                <tr key={index} onClick={() => {handleSelectPlayer(playerSeason.player_name)}}>
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