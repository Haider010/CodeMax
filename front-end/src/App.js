import React from 'react';
import Users from './components/Users';
import Problems from './components/Problems';
import Contests from './components/Contests';

const App = () => {
  return (
    <div>
      <h1>CodeMax Frontend</h1>
      <Users />
      <Problems />
      <Contests />
    </div>
  );
};

export default App;
