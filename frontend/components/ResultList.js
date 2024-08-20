import React from 'react';

function ResultList({ results, setDrel, setDirel }) {
    const toggleSelection = (id, list, setList) => {
        if (list.includes(id)) {
            setList(list.filter(item => item !== id));
        } else {
            setList([...list, id]);
        }
    };

    return (
        <ul>
            {results.map(result => (
                <li key={result.id}>
                    <input
                        type="checkbox"
                        checked={setDrel.includes(result.id)}
                        onChange={() => toggleSelection(result.id, setDrel, setDrel)}
                    /> Drel
                    <input
                        type="checkbox"
                        checked={setDirel.includes(result.id)}
                        onChange={() => toggleSelection(result.id, setDirel, setDirel)}
                    /> Direl
                    {result.text} (Score: {result.score})
                </li>
            ))}
        </ul>
    );
}

export default ResultList;
