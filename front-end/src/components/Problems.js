import React, { useState, useEffect } from 'react';
import { fetchProblems, addProblem } from '../services/api';

const Problems = () => {
  const [problems, setProblems] = useState([]);
  const [newProblem, setNewProblem] = useState({ title: '', difficulty: '', description: '' });

  useEffect(() => {
    fetchProblems().then((response) => setProblems(response.data.problems));
  }, []);

  const handleAddProblem = () => {
    addProblem(newProblem).then(() => {
      setNewProblem({ title: '', difficulty: '', description: '' });
      fetchProblems().then((response) => setProblems(response.data.problems));
    });
  };

  return (
    <div>
      <h2>Problems</h2>
      <ul>
        {problems.map((problem) => (
          <li key={problem.id}>
            {problem.title} - {problem.difficulty}
            <p>{problem.description}</p>
          </li>
        ))}
      </ul>
      <div>
        <input
          type="text"
          placeholder="Title"
          value={newProblem.title}
          onChange={(e) => setNewProblem({ ...newProblem, title: e.target.value })}
        />
        <input
          type="text"
          placeholder="Difficulty"
          value={newProblem.difficulty}
          onChange={(e) => setNewProblem({ ...newProblem, difficulty: e.target.value })}
        />
        <textarea
          placeholder="Description"
          value={newProblem.description}
          onChange={(e) => setNewProblem({ ...newProblem, description: e.target.value })}
        />
        <button onClick={handleAddProblem}>Add Problem</button>
      </div>
    </div>
  );
};

export default Problems;
