import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Editor } from '@monaco-editor/react';
import './styles/ProblemDetails.css';

const ProblemDetails = () => {
  const { id } = useParams();
  const [problem, setProblem] = useState(null);
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [submissionResult, setSubmissionResult] = useState([]);
  const [submissions, setSubmissions] = useState([]);  // New state for submissions
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showCodeModal, setShowCodeModal] = useState(false);  // To toggle the modal
  const [modalCode, setModalCode] = useState('');  // To store the code to be displayed in modal

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

    // Fetch submissions by problem ID
    fetch(`http://localhost:5000/submissions/${id}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.submissions && data.submissions.length > 0) {
          setSubmissions(data.submissions);
        } else {
          setSubmissions([]);
        }
      })
      .catch((error) => console.error('Error fetching submissions:', error));
  }, [id]);

  const handleCodeSubmit = () => {
    const userLoggedIn = localStorage.getItem('userLoggedIn') === 'true';
    
    if (!userLoggedIn) {
      setSubmissionResult([{ error: 'Please log in to submit code.' }]);
      return;
    }
  
    const payload = { code, language };
  
    setIsLoading(true);
    fetch(`http://localhost:5000/submitCode/${id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.test_case_results) {
          setSubmissionResult(data.test_case_results);
        } else if (data.error) {
          setSubmissionResult([{ error: data.error }]);
        } else {
          setSubmissionResult([{ error: 'Unexpected response format.' }]);
        }
      })
      .catch(() => setSubmissionResult([{ error: 'Submission failed.' }]))
      .finally(() => setIsLoading(false));
  };

  const openModal = (code) => {
    setModalCode(code);
    setShowCodeModal(true);
  };

  const closeModal = () => {
    setShowCodeModal(false);
  };

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!problem) {
    return <div>Loading problem details...</div>;
  }

  return (
    <div className="problem-page">
      {/* Problem Details */}
      <div className="problem-card">
        <h2 className="problem-title">{problem.title}</h2>
        <p className={`problem-difficulty ${problem.difficulty.toLowerCase()}`}>{problem.difficulty}</p>
        <p className="problem-description ">{problem.description}</p>
        {problem.example_input_output && (
          <div className="problem-example">
            <h3>Example</h3>
            <pre>{problem.example_input_output}</pre>
          </div>
        )}
      </div>

      {/* Submission Section */}
      <div className="submission-container">
        <div className="code-editor-container">
          <div className="editor-header">
            <span className="editor-title">Code Editor</span>
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
          <Editor
            height="400px"
            language={language}
            value={code}
            onChange={(newValue) => setCode(newValue)}
            theme="vs-dark"
          />
          <button className="submit-btn" onClick={handleCodeSubmit}>
            Submit Code
          </button>
        </div>

        <div className="submission-results">
          <h3>Submission Results</h3>
          {isLoading && <div className="loading-spinner"></div>}
          {!isLoading && submissionResult.length > 0 && (
            submissionResult.map((result, index) => (
              <div key={index} className="test-case-result">
                {result.error ? (
                  <p className="error">{result.error}</p>
                ) : (
                  <>
                    <p><strong>Input:</strong> {result.input}</p>
                    <p><strong>Expected Output:</strong> {result.expected_output}</p>
                    <p><strong>Your Output:</strong> {result.actual_output}</p>
                    <p className="status">
                      <strong>Status:</strong> 
                      {result.status === 'Accepted' ? (
                        <span className="status-accepted">
                          ✔️ {result.status}
                        </span>
                      ) : (
                        <span className="status-rejected">
                          ❌ {result.status}
                        </span>
                      )}
                    </p>
                    <p><strong>Execution Time:</strong> {result.execution_time}</p>
                    <p><strong>Memory:</strong> {result.memory}</p>
                  </>
                )}
              </div>
            ))
          )}
        </div>

        {/* Submissions Section */}
        <div className="submissions-list">
          <h3>All Submissions</h3>
          {submissions.length === 0 ? (
            <p>No submissions yet.</p>
          ) : (
            submissions.map((submission, index) => (
              <div key={index} className="submission-item">
                <div className="submission-row">
                  <p><strong>ID:</strong> {submission.id}</p>
                  <p><strong>Language:</strong> {submission.language}</p>
                  <p><strong>Status:</strong> {submission.status}</p>
                  <p><strong>Submission Date:</strong> {submission.submitted_at}</p>
                  <button className="view-code" onClick={() => openModal(submission.code)}>
                    View Code
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Modal for Code */}
      {showCodeModal && (
        <div className="code-modal">
          <div className="modal-content">
            <span className="close" onClick={closeModal}>&times;</span>
            <h4>Code</h4>
            <pre>{modalCode}</pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProblemDetails;
