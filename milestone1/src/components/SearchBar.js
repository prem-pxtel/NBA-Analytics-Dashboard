import React, { useState } from 'react';

const SearchBar = ({handleSearch}) => {
  const [searchTerm, setSearchTerm] = useState('');

  const onSubmit = (e) => {
    e.preventDefault();
    handleSearch(searchTerm);
  };

  return (
    <form onSubmit={onSubmit}>
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Search Players!"
      />
      <button type="submit">Search</button>
    </form>
  );
}

export default SearchBar;