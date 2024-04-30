import React, { useState } from 'react';
import { put } from 'aws-amplify/api';

function App() {
  const [formData, setFormData] = useState({
    name: '',
    gender: '',
    topic: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await put({
        apiName: "bookstoreapi",
        path: "/book/123",
        options: {
          body: { formData },
        }
      });
      
      console.log('Response:', response);
      // Optionally, reset the form after successful submission
      setFormData({
        name: '',
        gender: '',
        topic: ''
      });
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <><link rel="stylesheet" href="./styles.css" /><div className="App">
      <h1>Submit Form</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange} />
        </div>
        <div>
          <label htmlFor="gender">Gender:</label>
          <input
            type="text"
            id="gender"
            name="gender"
            value={formData.gender}
            onChange={handleChange} />
        </div>
        <div>
          <label htmlFor="topic">Topic:</label>
          <input
            type="text"
            id="topic"
            name="topic"
            value={formData.topic}
            onChange={handleChange} />
        </div>
        <button type="submit">Submit</button>
      </form>
    </div></>
  );
}

// export default App;


export default App;
