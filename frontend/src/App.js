import './App.css';
import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import PlayersList from './components/PlayersList';
import PlayerGameList from './components/PlayerGameList';
import BestGame from './components/BestGame';
import TopPlayers from './components/TopPlayers';





function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [players, setPlayers] = useState([])
  const [selectedPlayer, setSelectedPlayer] = useState(null)

  const handleSearch = (term) => {
    setSearchTerm(term);
    setSelectedPlayer(null);
    console.log("Searching for:", term);
    
  };

  const handleSelectPlayer = (playerName) => {
    console.log("player name", playerName)
    setSelectedPlayer(playerName);
  }

  return (
    <div className="App">
      <SearchBar handleSearch={handleSearch} />
      {searchTerm && <PlayersList searchTerm={searchTerm} handleSelectPlayer={handleSelectPlayer} />}
      {selectedPlayer && <PlayerGameList selectedPlayer={selectedPlayer}/>}
      {selectedPlayer && <BestGame selectedPlayer={selectedPlayer}/>}
      <TopPlayers />
    </div>
  );
}

export default App;