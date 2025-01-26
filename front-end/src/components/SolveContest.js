import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { getContestProblems, getContestByID } from "../services/api";
import { Editor } from "@monaco-editor/react";
import { useNavigate } from 'react-router-dom';
import "./styles/SolveContest.css";

const SolveContest = () => {
  const navigate = useNavigate();
  const { contestId } = useParams();
  const [problems, setProblems] = useState([]);
  const [error, setError] = useState(null);
  const [selectedProblemIndex, setSelectedProblemIndex] = useState(0);
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [submissionResult, setSubmissionResult] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [timeTaken, setTimeTaken] = useState(0);
  const [remainingTime, setRemainingTime] = useState(0);
  const [acceptedCount, setAcceptedCount] = useState(0);
  useEffect(() => {
    const userLoggedIn = localStorage.getItem("userLoggedIn") === "true";

    if (!userLoggedIn) {
      // Redirect to login if the user is not logged in
      navigate("/login");
    } else {
      const userName = localStorage.getItem("userName");
      if (contestId && userName) {

        fetch(`http://localhost:5000/has_finished_contest?contestId=${contestId}&userName=${userName}`)
          .then((response) => response.json())
          .then((data) => {
            if (data.finished) {
              // Redirect to another page (e.g., home page or contest finished page)
              navigate("/contestFinished");
            }
          })
          .catch(() => {
            // Handle error (optional)
            console.log("Error checking contest status.");
          });
      }
    }
  }, [contestId, navigate]); // Include contestId in the dependency array
  
  

   // Count of accepted submissions

  useEffect(() => {
    getContestProblems(contestId)
      .then((response) => {
        if (response.data.contest_problems) {
          setProblems(response.data.contest_problems);
        }
      })
      .catch(() => setError("Failed to load contest problems."));

    getContestByID(contestId)
      .then((response) => {
        const endTimeString = response.data.contest["End-Time"];
        const formattedEndTimeString =
          endTimeString.includes(":") && !endTimeString.includes(":00")
            ? endTimeString + ":00"
            : endTimeString;
        const contestEndTime = new Date(formattedEndTimeString + "Z").getTime();
        setRemainingTime(
          Math.floor((contestEndTime - new Date().getTime()) / 1000)
        );
      })
      .catch(() => setError("Failed to load contest details."));
  }, [contestId]);

  useEffect(() => {
    const startTime = localStorage.getItem("startTime");
    if (startTime) {
      const interval = setInterval(() => {
        const currentTime = new Date().getTime();
        const timeElapsed = Math.floor(
          (currentTime - new Date(startTime).getTime()) / 1000
        );
        setTimeTaken(timeElapsed);
      }, 1000);

      return () => clearInterval(interval);
    }
  }, []);

  useEffect(() => {
    if (remainingTime > 0) {
      const interval = setInterval(() => {
        setRemainingTime((prevTime) => (prevTime > 0 ? prevTime - 1 : 0));
      }, 1000);

      return () => clearInterval(interval);
    }
  }, [remainingTime]);

  const formatTime = (milliseconds) => {
    const hours = Math.floor(milliseconds / (1000 * 60 * 60));
    const minutes = Math.floor((milliseconds % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((milliseconds % (1000 * 60)) / 1000);
    return `${hours}:${minutes}:${seconds}`;
  };

  const handleTabClick = (index) => {
    setSelectedProblemIndex(index);
    setCode("");
    setSubmissionResult([]);
  };

  const handleCodeSubmit = () => {
    const userLoggedIn = localStorage.getItem("userLoggedIn") === "true";

    if (!userLoggedIn) {
      setSubmissionResult([{ error: "Please log in to submit code." }]);
      return;
    }

    const problemId = problems[selectedProblemIndex]?.id;
    const payload = { code, language };

    setIsLoading(true);
    fetch(`http://localhost:5000/submitCode/${problemId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.test_case_results) {
          setSubmissionResult(data.test_case_results);

          // Count accepted submissions
          const accepted = data.test_case_results.some(
            (result) => result.status === "Accepted"
          );
          if (accepted) {
            setAcceptedCount((prevCount) => prevCount + 1);
          }
        } else if (data.error) {
          setSubmissionResult([{ error: data.error }]);
        } else {
          setSubmissionResult([{ error: "Unexpected response format." }]);
        }
      })
      .catch(() => setSubmissionResult([{ error: "Submission failed." }]))
      .finally(() => setIsLoading(false));
  };

  const handleFinishContest = () => {
    // Retrieve the user's name from localStorage
    const userName = localStorage.getItem("userName");
  
    // Prepare the payload including the user's name
    const payload = {
      contestId: contestId,
      totalTimeTaken: timeTaken,
      acceptedSubmissions: acceptedCount,
      userName: userName, // Add user's name here
    };
  
    // Send the data to the backend
    fetch("http://localhost:5000/finishContest", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Contest finished! Your results have been saved.");
        } else {
          alert("Failed to finish the contest. Try again.");
        }
      })
      .catch(() => alert("Error occurred while finishing the contest."));
  };
  

  return (
    
    <div className="solve-contest-container">
      <h2>Contest Problems</h2>
      {error ? (
        <p className="error-message">{error}</p>
      ) : (
        <div className="tabs-container">
          <div className="tabs">
            {problems.length === 0 ? (
              <p>No problems found for this contest.</p>
            ) : (
              problems.map((problem, index) => (
                <button
                  key={problem.id}
                  className={`tab ${selectedProblemIndex === index ? "active" : ""}`}
                  onClick={() => handleTabClick(index)}
                >
                  Problem-{index + 1}
                </button>
              ))
            )}
          </div>
          <div className="top-section">
        <button className="finish-button" onClick={handleFinishContest}>
          Finish Contest 🎉
        </button>
      </div>
          {problems.length > 0 && (
            <>
              <div className="problem-details">
                <h3>{problems[selectedProblemIndex].title}</h3>
                <p>{problems[selectedProblemIndex].description}</p>
                <p>
                  <strong>Difficulty:</strong>{" "}
                  {problems[selectedProblemIndex].difficulty}
                </p>
                <p>
                  <strong>Example:</strong>{" "}
                  {problems[selectedProblemIndex].example}
                </p>
              </div>

              <div className="time-taken">
                <strong>Time Taken: </strong>
                {formatTime(timeTaken * 1000)}
              </div>

              <div className="remaining-time">
                <strong>Remaining Time: </strong>
                {formatTime(remainingTime * 1000)}
              </div>

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
                {!isLoading &&
                  submissionResult.length > 0 &&
                  submissionResult.map((result, index) => (
                    <div key={index} className="test-case-result">
                      {result.error ? (
                        <p className="error">{result.error}</p>
                      ) : (
                        <>
                          <p>
                            <strong>Input:</strong> {result.input}
                          </p>
                          <p>
                            <strong>Expected Output:</strong>{" "}
                            {result.expected_output}
                          </p>
                          <p>
                            <strong>Your Output:</strong> {result.actual_output}
                          </p>
                          <p className="status">
                            <strong>Status:</strong>
                            {result.status === "Accepted" ? (
                              <span className="status-accepted">
                                ✔️ {result.status}
                              </span>
                            ) : (
                              <span className="status-rejected">
                                ❌ {result.status}
                              </span>
                            )}
                          </p>
                          <p>
                            <strong>Execution Time:</strong>{" "}
                            {result.execution_time}
                          </p>
                          <p>
                            <strong>Memory:</strong> {result.memory}
                          </p>
                        </>
                      )}
                    </div>
                  ))}
              </div>

            </>
          )}
        </div>
      )}
    </div>
  );
};

export default SolveContest;
