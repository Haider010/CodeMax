import React, { useState, useEffect } from 'react';
import { fetchUsers, addUser } from '../services/api';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState({ name: '', email: '' });

  useEffect(() => {
    fetchUsers().then((response) => setUsers(response.data.users));
  }, []);

  const handleAddUser = () => {
    addUser(newUser).then(() => {
      setNewUser({ name: '', email: '' });
      fetchUsers().then((response) => setUsers(response.data.users));
    });
  };

  return (
    <div>
      <h2>Users</h2>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name} ({user.email})</li>
        ))}
      </ul>
      <div>
        <input
          type="text"
          placeholder="Name"
          value={newUser.name}
          onChange={(e) => setNewUser({ ...newUser, name: e.target.value })}
        />
        <input
          type="email"
          placeholder="Email"
          value={newUser.email}
          onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
        />
        <button onClick={handleAddUser}>Add User</button>
      </div>
    </div>
  );
};

export default Users;
