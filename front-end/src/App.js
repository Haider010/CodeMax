import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Users from './components/Users';
import Problems from './components/Problems';
import Contests from './components/Contests';
import Register from './components/Register';
import Login from './components/Login';
import ProblemDetails from './components/ProblemDetails'; // Import ProblemDetails
import './App.css'; // Make sure the CSS file is imported

const App = () => {
  return (
    <Router>
      <div>
        <header>
          <h1>CodeMax</h1>
          <nav>
            <div className="left-links">
              <Link to="/">Home</Link> |  
              <Link to="/problems">Problems</Link> |  
              <Link to="/contests">Contests</Link>
            </div>
            <div className="right-links">
              <Link to="/register">Register</Link> |  
              <Link to="/login">Login</Link>
            </div>
          </nav>
        </header>

        <main>
          <Routes>
            {/* Home page */}
            <Route
              path="/"
              element={<h2>Welcome to CodeMax! Choose an option from the navigation above.</h2>}
            />

            {/* Existing components */}
            <Route path="/users" element={<Users />} />
            <Route path="/problems" element={<Problems />} />
            <Route path="/contests" element={<Contests />} />

            {/* Login and Registration components */}
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />

            {/* ProblemDetails route for viewing problem details */}
            <Route path="/problems/:id" element={<ProblemDetails />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
