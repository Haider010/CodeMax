import React from 'react';
import { useNavigate } from 'react-router-dom';

const ContestFinished = () => {
  const navigate = useNavigate();

  return (
    <div className="contest-finished">
      <h2>Contest Finished</h2>
      <p>You have already finished this contest. Thank you for participating!</p>
      <button onClick={() => navigate("/")}>Go to Home</button>
    </div>
  );
};

export default ContestFinished;
