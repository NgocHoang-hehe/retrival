import React, { useState } from 'react';
import axios from 'axios';

function SearchForm({ setResults }) {
    const [query, setQuery] = useState('');
    const [Drel, setDrel] = useState([]);
    const [Direl, setDirel] = useState([]);

    const handleSearch = () => {
        axios.post('http://localhost:5000/search', {
            query: query,
            Drel: Drel,
            Direl: Direl
        }).then(response => {
            setResults(response.data.results);
        });
    };

    return (
        <div>
            <input type="text" value={query} onChange={e => setQuery(e.target.value)} />
            <button onClick={handleSearch}>Search</button>
        </div>
    );
}

export default SearchForm;
