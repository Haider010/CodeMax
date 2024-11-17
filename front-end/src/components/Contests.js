import React, { useState, useEffect } from 'react';
import { fetchContests, addContest } from '../services/api';

const Contests = () => {
  const [contests, setContests] = useState([]);
  const [newContest, setNewContest] = useState({ title: '', description: '', start_time: '', end_time: '', status: '' });

  useEffect(() => {
    fetchContests().then((response) => setContests(response.data.contests));
  }, []);

  const handleAddContest = () => {
    addContest(newContest).then(() => {
      setNewContest({ title: '', description: '', start_time: '', end_time: '', status: '' });
      fetchContests().then((response) => setContests(response.data.contests));
    });
  };

  return (
    <div>
      <h2>Contests</h2>
      <ul>
  {contests.map((contest) => (
    <li key={contest.id}>
      {contest.title} - {contest.description} - {contest.start_time} to {contest.end_time} - Status: {contest.status} - Created At: {contest.created_at}
    </li>
  ))}
</ul>
      <div>
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
        <input
          type="datetime-local"
          placeholder="Start Time"
          value={newContest.start_time}
          onChange={(e) => setNewContest({ ...newContest, start_time: e.target.value })}
        />
        <input
          type="datetime-local"
          placeholder="End Time"
          value={newContest.end_time}
          onChange={(e) => setNewContest({ ...newContest, end_time: e.target.value })}
        />
        <input
          type="text"
          placeholder="Status"
          value={newContest.status}
          onChange={(e) => setNewContest({ ...newContest, status: e.target.value })}
        />
        <button onClick={handleAddContest}>Add Contest</button>
      </div>
    </div>
  );
};

export default Contests;
