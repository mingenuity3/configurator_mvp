import React, { useState } from 'react';
import { post } from 'aws-amplify/api';

function App() {
  const [question] = useState("Wer ist der coolste hier?");
  const [selectedOption, setSelectedOption] = useState(null);
  const [options] = useState([
    { id: 1, text: 'Marc' },
    { id: 2, text: 'Matthias' },
    { id: 3, text: 'Matthes' },
  ]);

  const handleOptionSelect = (optionText) => {
    setSelectedOption(optionText);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await post({
        apiName: "bookstoreapi",
        path: "/book/123",
        options: {
          body: { selectedOption },
        }
      });
      
      console.log('Request:', selectedOption);
      console.log('Response:', response);
      // Optionally, reset the form after successful submission
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <><link rel="stylesheet" href="./styles.css" /><div className="App">
      <h1>{question}</h1>
      <form onSubmit={handleSubmit}>
        <ul>
        {options.map((option) => (
          <li
            key={option.id}
            className={selectedOption === option.text ? 'selected' : ''}
            onClick={() => handleOptionSelect(option.text)}
          >
            {option.text}
          </li>
        ))}
        </ul>
        {selectedOption && (
        <p>
          Ausgesucht: {selectedOption}
        </p>
        )}
        <button type="submit">Ab inne Datenbank</button>
      </form>
    </div></>
  );
}

// export default App;


export default App;
