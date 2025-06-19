import './App.css';
import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import PlayersList from './components/PlayersList';


function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [players, setPlayers] = useState([])

  const handleSearch = (term) => {
    setSearchTerm(term);
    console.log("Searching for:", term);
    
  };

  return (
    <div className="App">
      <SearchBar handleSearch={handleSearch} />
      {searchTerm && <PlayersList searchTerm={searchTerm}/>}
    </div>
  );
}

export default App;