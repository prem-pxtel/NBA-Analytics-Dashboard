import React, {useState, useEffect} from 'react'

const PlayersList = ({searchTerm}) => {
    const [playersData, setPlayersData] = useState([]);

    useEffect(() => {
        console.log('use eff')
        setPlayersData([{year: 2004, "points_per_game": 24, "assists_per_game": 12, "rebounds_per_game": 5, "blocks_per_game": 3}]);
        return;
    }, [searchTerm])

    return (
        <div>
            {playersData.length != 0 ? (
                <table className="players-table">
                    <thead>
                        <tr>
                            <th>Season</th>
                            <th>Points per game</th>
                            <th>Assists per game</th>
                            <th>Rebounds per game</th>
                            <th>Blocks per game</th>
                        </tr>
                    </thead>
                    <tbody>
                        {playersData.map((playerSeason, index) => (
                            <tr key={index}>
                                <td>{playerSeason.year}</td>
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

export default PlayersList