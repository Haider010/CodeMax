import React, { useState, useEffect } from 'react';
import { fetchProblems, addProblem } from '../services/api';
import './styles/Problems.css';

const Problems = () => {
  const [problems, setProblems] = useState([]);
  const [newProblem, setNewProblem] = useState({ title: '', difficulty: '', description: '' });
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchProblems().then((response) => setProblems(response.data.problems));
  }, []);

  const handleAddProblem = async (e) => {
    e.preventDefault();
    try {
      await addProblem(newProblem);
      setMessage('Problem added successfully!');
      setNewProblem({ title: '', difficulty: '', description: '' });
      fetchProblems().then((response) => setProblems(response.data.problems));
    } catch (error) {
      setMessage('Failed to add problem. Please try again.');
    }
  };

  return (
    <div className="problems-container">
      <h2>Problems</h2>

      {/* Display Problems */}
      <table className="problems-table">
        <thead>
          <tr>
            <th>Problem No</th> {/* New Column Header */}
            <th>Title</th>
            <th>Difficulty</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {problems.map((problem, index) => (
            <tr key={problem.id}>
              <td>{index + 1}</td> {/* Displaying Problem ID */}
              <td>{problem.title}</td>
              <td>
                <span
                  className={`difficulty ${problem.difficulty.toLowerCase()}`}
                >
                  {problem.difficulty}
                </span>
              </td>
              <td>{problem.description}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Add Problem Section */}
      <div className="add-problem-container">
        <h3>Add a New Problem</h3>
        <form className="add-problem-form" onSubmit={handleAddProblem}>
          <input
            type="text"
            placeholder="Title"
            value={newProblem.title}
            onChange={(e) => setNewProblem({ ...newProblem, title: e.target.value })}
            required
          />
          <select
            value={newProblem.difficulty}
            onChange={(e) => setNewProblem({ ...newProblem, difficulty: e.target.value })}
            required
          >
            <option value="">Select Difficulty</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
          <textarea
            placeholder="Description"
            value={newProblem.description}
            onChange={(e) => setNewProblem({ ...newProblem, description: e.target.value })}
            required
          />
          <button type="submit">Add Problem</button>
        </form>
        {message && <p className="message">{message}</p>}
      </div>
    </div>
  );
};

export default Problems;
