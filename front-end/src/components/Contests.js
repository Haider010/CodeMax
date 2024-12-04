import React, { useState, useEffect } from 'react';
import { fetchContests, addContest } from '../services/api';
import './styles/Contests.css';

const Contests = () => {
  const [contests, setContests] = useState([]);
  const [newContest, setNewContest] = useState({ title: '', description: '', start_time: '', end_time: '' });
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchContests().then((response) => setContests(response.data.contests));
  }, []);

  const handleAddContest = () => {
    const currentTime = new Date().toISOString();
    const { start_time, end_time } = newContest;

    if (start_time <= currentTime) {
      setError("Start time must be in the future.");
      return;
    }
    if (start_time >= end_time) {
      setError("Start time must be before end time.");
      return;
    }

    setError(null); // Clear error before submitting

    addContest(newContest)
      .then(() => {
        setNewContest({ title: '', description: '', start_time: '', end_time: '' });
        fetchContests().then((response) => setContests(response.data.contests));
      })
      .catch((err) => setError(err.response.data.error));
  };

  return (
    <div className="contests-container">
      <h2>Contests</h2>
      <div className="contests-list">
        {contests.length === 0 ? (
          <p>No contests available. Add some!</p>
        ) : (
          contests.map((contest) => (
            <div key={contest.id} className="contest-card">
              <h3>{contest.title}</h3>
              <p>{contest.description}</p>
              <p>
                <strong>Start:</strong> {contest.start_time}
              </p>
              <p>
                <strong>End:</strong> {contest.end_time}
              </p>
              <p>
                <strong>Status:</strong> {contest.status}
              </p>
              <p>
                <strong>Created At:</strong> {contest.created_at}
              </p>
            </div>
          ))
        )}
      </div>
      <div className="add-contest-section">
        <h3>Add a New Contest</h3>
        <input
          type="text"
          placeholder="Title"
          value={newContest.title}
          onChange={(e) => setNewContest({ ...newContest, title: e.target.value })}
        />
        <textarea
          placeholder="Description"
          value={newContest.description}
          onChange={(e) => setNewContest({ ...newContest, description: e.target.value })}
        />
        <div className="datetime-container">
          <input
            type="datetime-local"
            placeholder="Start Time"
            value={newContest.start_time}
            onChange={(e) => setNewContest({ ...newContest, start_time: e.target.value })}
          />
          {error && error.includes("Start time must be in the future.") && (
            <p className="error-message">{error}</p>
          )}
        </div>
        <div className="datetime-container">
          <input
            type="datetime-local"
            placeholder="End Time"
            value={newContest.end_time}
            onChange={(e) => setNewContest({ ...newContest, end_time: e.target.value })}
          />
          {error && error.includes("Start time must be before end time.") && (
            <p className="error-message">{error}</p>
          )}
        </div>
        <button onClick={handleAddContest}>Add Contest</button>
      </div>
    </div>
  );
};

export default Contests;
