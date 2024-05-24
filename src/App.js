import React, { useState, useEffect } from 'react';
import { post, get, put } from 'aws-amplify/api';
import './App.css'; // Assuming you have some CSS to style your component

const App = () => {
  const initialQuestions = [
    { id: 1, type: 'options', text: 'Wer ist der Hauptcharakter?', options: ['Mädchen', 'Junge', 'Tier'], category: "gender", selectedOption: '' },
    { id: 2, type: 'text', text: 'Wie heißt denn unser:e Hauptcharakter?', category: "name", selectedOption: '' },
    { id: 3, type: 'options', text: 'Welche Werte möchtest du mit deinem Buch vermitteln?', category: "value", options: ['Mut', 'Freundschaft', 'Akzeptanz'], selectedOption: '' },
    { id: 4, type: 'options', text: 'Welche Situation soll gelöst werden?', category: "issue", options: ['Der erste Tag im Kindergarten.', 'Das erst Mal Fahrradfahren.', 'Unser erster Urlaub.'], selectedOption: '' },
    { id: 5, type: 'options-llm', text: 'Wo spielt die Geschichte?', category: "setting", options: ['loading'], selectedOption: '' }
  ];

  const [questions, setQuestions] = useState(initialQuestions);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [summaryRequested, setSummaryRequested] = useState(false);
  const [storyId, setStoryId] = useState('');
  const [summary, setSummary] = useState('');

  useEffect(() => {
    const loadLlmOptions = async () => {
      const currentQuestion = questions[currentQuestionIndex];
      if (currentQuestion.type === 'options-llm') {
        const previousSelections = questions.slice(0, currentQuestionIndex).reduce((acc, question) => {
          acc[question.category] = question.selectedOption;
          return acc;
        }, {});

        try {
          const restOperation = post({
            apiName: "bookstoreapi",
            path: "/generated-answers",
            options: {
              body: previousSelections,
            }
          });
          
          const { body } = await restOperation.response;
          const newOptions = await body.json();
          
          console.log(newOptions);
          console.log(questions);
          console.log(previousSelections);

          setQuestions(prevQuestions => {
            const updatedQuestions = [...prevQuestions];
            updatedQuestions[currentQuestionIndex].options = newOptions;
            return updatedQuestions;
          });

        } catch (error) {
          console.error('Error fetching options:', error);
        }
      }
    };

    loadLlmOptions();
  }, [currentQuestionIndex]);

  useEffect(() => {
      if (allQuestionsAnswered) {
      handleSubmit();
    }
  }, [questions]);

  const handleOptionClick = (option) => {
    const updatedQuestions = [...questions];
    updatedQuestions[currentQuestionIndex].selectedOption = option;
    setQuestions(updatedQuestions);

    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const handleTextChange = (event) => {
    const updatedQuestions = [...questions];
    updatedQuestions[currentQuestionIndex].selectedOption = event.target.value;
    setQuestions(updatedQuestions);
  };

  const handleTextSubmit = (event) => {
    event.preventDefault();
    if (questions[currentQuestionIndex].selectedOption.trim() !== '') {
      if (currentQuestionIndex < questions.length - 1) {
        setCurrentQuestionIndex(currentQuestionIndex + 1);
      }
    }
  };

  const allQuestionsAnswered = questions.every(q => q.selectedOption !== '');

  const handleSubmit = async () => {
    if (allQuestionsAnswered) {
      try {
        setIsSubmitted(true);
        const categorySelectedOptionPairs = {};
        questions.forEach(question => {
          categorySelectedOptionPairs[question.category] = question.selectedOption;
        });
      
        console.log('Request:', categorySelectedOptionPairs);

        const restOperation = post({
          apiName: "bookstoreapi",
          path: "/book",
          options: {
            body: { categorySelectedOptionPairs },
          }
        });
        
        const {body}= await restOperation.response;
        const json = await body.json();

        console.log('Response:', json);
        setStoryId(json);

        } catch (error) {
        console.error('Error:', error);
      }
    }
  };

  const handleGenerateSummary = async () => {
    setSummaryRequested(true);
    try {
      const restOperation = get({
        apiName: "bookstoreapi",
        path: `/generated-story/${storyId}`,
      });
      
      const {body}= await restOperation.response;
      const json = await body.json();

      console.log('Generate Summary Response:', json);

      // Set the summary in state
      setSummary(json);
      saveSummary(json, storyId);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const saveSummary = async (summary, storyId) => {
    try {
      // Save summary to StoryId in DynamoDB
      const restOperation = put({
        apiName: "bookstoreapi",
        path: `/book/${storyId}`,
        options: {
          body: { summary },
        }
      });
      
      //const {body}= await restOperation2.response;
      //const json = await body.json();

    } catch (error) {
      console.error('Error:', error);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <img src="/fabula_logo.png" alt="Fabula Logo" className="logo" />
      </header>
      {!allQuestionsAnswered && (
        <div className="question-container">
          {questions.slice(currentQuestionIndex, currentQuestionIndex + 1).map((question, index) => (
            <div key={question.id} className="question-block">
              <h2>{question.text}</h2>
              {question.type === 'options' ? (
                <div className="options">
                  {question.options.map(option => (
                    <button
                      key={option}
                      className={`option ${question.selectedOption === option ? 'selected' : ''}`}
                      onClick={() => handleOptionClick(option)}
                      disabled={question.selectedOption !== ''}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              ) : question.type === 'text' ? (
                <form onSubmit={handleTextSubmit}>
                  <input
                    type="text"
                    value={question.selectedOption}
                    onChange={handleTextChange}
                    className="text-input"
                  />
                  <button type="submit" className="submit-text-button">
                    Bestätigen
                  </button>
                </form>
              ) : question.type === 'options-llm' ? (
                <div className="options">
                  {question.options.map(option => (
                    <button
                      key={option}
                      className={`option ${question.selectedOption === option ? 'selected' : ''}`}
                      onClick={() => handleOptionClick(option)}
                      disabled={question.selectedOption !== ''}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              ) : null}
            </div>
          ))}
        </div>
      )}
      {allQuestionsAnswered && !summaryRequested && (
        <div className="book">
          <h2>Deine Auswahl</h2>
          {questions.map((question, index) => (
            <p key={question.id}>
              <strong>{question.text}</strong> {question.selectedOption}
            </p>
          ))}
          <button className="submit-button" onClick={handleGenerateSummary}>
            Zusammenfassung erstellen
          </button>
        </div>
      )}
      {summaryRequested && (
        <div className="book">
          <p key="summary-area">
            <strong>Buchzusammenfassung</strong>
          </p>
          <textarea
              className="summary-textarea"
              value={summary}
              readOnly
          />
        </div>
      )}
    </div>
  );
};

export default App;
