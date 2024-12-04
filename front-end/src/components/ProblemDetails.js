import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Editor } from '@monaco-editor/react';
import './styles/ProblemDetails.css';

const ProblemDetails = () => {
  const { id } = useParams(); // Get the problem ID from the URL
  const [problem, setProblem] = useState(null);
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [submissionResult, setSubmissionResult] = useState('');
  const [error, setError] = useState(null);

  // Fetch problem details by ID
  useEffect(() => {
    fetch(`http://localhost:5000/Problems/${id}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Problem not found');
        }
        return response.json();
      })
      .then((data) => setProblem(data))
      .catch((error) => setError(error.message));
  }, [id]);

  const handleCodeSubmit = () => {
    const payload = { code, language };

    fetch('http://localhost:5000/submitCode', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
      .then((response) => response.json())
      .then((data) => setSubmissionResult(data.result))
      .catch(() => setSubmissionResult('Submission failed.'));
  };

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!problem) {
    return <div>Loading problem details...</div>;
  }

  return (
    <div className="problem-details-container">
      {/* Problem Details Section */}
      <div className="problem-details">
        <h2>{problem.title}</h2>
        <p className="difficulty">
          Difficulty:{' '}
          <span className={problem.difficulty.toLowerCase()}>{problem.difficulty}</span>
        </p>
        <p className="description">{problem.description}</p>
        
        {/* Example Section */}
        {problem.example_input_output && (
          <div className="example-section">
            <h3>Example</h3>
            <pre className="example">{problem.example_input_output}</pre>
          </div>
        )}
      </div>

      {/* Code Editor Section */}
      <div className="code-editor">
        <div className="code-header">
          <span>Selected Language: {language}</span>
          <select
            className="language-select"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="java">Java</option>
            <option value="cpp">C++</option>
            <option value="csharp">C#</option>
          </select>
        </div>
        
        {/* Monaco Editor */}
        <div className="editor-container">
          <Editor
            height="400px"
            language={language}
            value={code}
            onChange={(newValue) => setCode(newValue)}
            theme="vs-dark"
          />
        </div>

        <button className="submit-button" onClick={handleCodeSubmit}>
          Submit
        </button>
        {submissionResult && <p className="submission-result">{submissionResult}</p>}
      </div>
    </div>
  );
};

export default ProblemDetails;
