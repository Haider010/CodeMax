import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom
import { fetchProblems } from '../services/api';
import './styles/Problems.css';

const Problems = () => {
  const [problems, setProblems] = useState([]);

  useEffect(() => {
    fetchProblems().then((response) => setProblems(response.data.problems));
  }, []);

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
            <th> </th> {/* New Column for Solve Link */}
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

              {/* Solve Column with Link */}
              <td>
                <Link to={`/Problems/${problem.id}`} className="solve-link">
                  Solve
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Problems;
