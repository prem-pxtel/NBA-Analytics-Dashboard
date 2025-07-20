import './App.css';
import React, { useState, useEffect } from 'react';
import Auth from './components/Auth';
import SearchBar from './components/SearchBar';
import PlayersList from './components/PlayersList';
import PlayerGameList from './components/PlayerGameList';
import BestGame from './components/BestGame';
import TopPlayers from './components/TopPlayers';
import MostRecent from './components/MostRecent';


function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [players, setPlayers] = useState([])
  const [selectedPlayer, setSelectedPlayer] = useState(null)

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = (token) => {
    // dont think we need the token but just incase
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setIsAuthenticated(false);
    setSearchTerm('');
    setSelectedPlayer(null);
  };

  const handleSearch = (term) => {
    setSearchTerm(term);
    setSelectedPlayer(null);
    console.log("Searching for:", term);
  };

  const handleSelectPlayer = (playerName) => {
    console.log("player name", playerName)
    setSelectedPlayer(playerName);
  }

  if (!isAuthenticated) {
    return <Auth onLogin={handleLogin} />;
  }

  return (
    <div className="App">
      <div style={{ padding: '15px', borderBottom: '1px solid #ccc', display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: "20px" }}>
        <h1 style={{ margin: 0 }}>CS348 Basketball Association</h1>
        <button 
          onClick={handleLogout}
          style={{ 
            padding: '8px 16px', 
            backgroundColor: 'red', 
            color: 'white', 
            border: 'none', 
            cursor: 'pointer' 
          }}
        >
          Logout
        </button>
      </div>
      <SearchBar handleSearch={handleSearch} />
      {searchTerm && <PlayersList searchTerm={searchTerm} handleSelectPlayer={handleSelectPlayer} />}
      {selectedPlayer && <PlayerGameList selectedPlayer={selectedPlayer}/>}
      {selectedPlayer && <BestGame selectedPlayer={selectedPlayer}/>}
      {selectedPlayer && <MostRecent selectedPlayer={selectedPlayer}/>}
      <TopPlayers />
    </div>
  );
}

export default App;