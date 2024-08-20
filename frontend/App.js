import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [showFeedback, setShowFeedback] = useState(false);

  const handleSearch = async () => {
    try {
      const response = await axios.post('http://localhost:5000/search', { query });
      setResults(response.data);
      setShowFeedback(true);
    } catch (error) {
      console.error('Error searching:', error);
    }
  };

  const handleFeedback = async () => {
    const relevantDocs = results
    .filter((result) => result.relevant) // Lọc những phần tử có `relevant` là true
    .map((result) => result.document); // Trả về dữ liệu thay vì index

    const irrelevantDocs = results
    .filter((result) => !result.relevant) // Lọc những phần tử có `relevant` là false
    .map((result) => result.document); // Trả về dữ liệu thay vì index

    try {
      const response = await axios.post('http://localhost:5000/feedback', {
        query,
        relevant_docs: relevantDocs,
        irrelevant_docs: irrelevantDocs,
      });
      setResults(response.data);
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  const toggleRelevance = (index) => {
    const updatedResults = [...results];
    updatedResults[index].relevant = !updatedResults[index].relevant;
    setResults(updatedResults);
  };

  return (
    <div className="App">
      <h1>Vietnamese Search System</h1>
      <div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query"
        />
        <button onClick={handleSearch}>Search</button>
      </div>
      {results.length > 0 && (
        <div>
          <h2>Results:</h2>
          <ul>
            {results.map((result, index) => (
              <li key={index}>
                <label>
                  <input
                    type="checkbox"
                    checked={result.relevant || false}
                    onChange={() => toggleRelevance(index)}
                  />
                  {result.document} (Score: {result.score.toFixed(4)})
                </label>
              </li>
            ))}
          </ul>
          {showFeedback && (
            <button onClick={handleFeedback}>Submit Feedback</button>
          )}
        </div>
      )}
    </div>
  );
}

export default App;