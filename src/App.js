import React, { useState } from 'react';
import { put } from 'aws-amplify/api';

// import { E5113, E5114, E5117, E5118, E6143, E6144, E6147, E6148, E6149 } from './children';

// const App = () => {
//   return (
//     <html lang="en">
//       <head>
//         <meta charset="utf-8" />
//         <title>Html Generated</title>
//         <meta name="description" content="Figma htmlGenerator" />
//         <meta name="author" content="htmlGenerator" />
//         <link href="https://fonts.googleapis.com/css?family=Inter&display=swap" rel="stylesheet" />
//         <link rel="stylesheet" href="./styles.css" />
//       </head>
//       <body>
//         <E5113>
//           <E5114>
//             <E5117>
//               <span className="e5118">Gordon</span>
//             </E5117>
//             <E6143>
//               <span className="e6144">Junge</span>
//             </E6143>
//             <E6147>
//               <span className="e6148">Mädchen</span>
//             </E6147>
//           </E5114>
//           <span className="e6149">Worum handelt es sich denn bei dem Hauptcharakter?</span>
//         </E5113>
//       </body>
//     </html>
//   );
// };


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
      const response = await put('childrenbookstoreapi', '/book/1', {
        body: { ...formData }
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
