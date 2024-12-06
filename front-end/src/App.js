import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useNavigate } from 'react-router-dom';
import Users from './components/Users';
import Problems from './components/Problems';
import Register from './components/Register';
import Login from './components/Login';
import ProblemDetails from './components/ProblemDetails';
import VerifyPage from './components/VerifyPage';
import Home from './components/Home';
import Study from './components/Study';
import AIAssist from './components/AiAssist'; // Import the AI Assist component
import './App.css';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const userLoggedIn = localStorage.getItem('userLoggedIn') === 'true';
    setIsLoggedIn(userLoggedIn);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('userLoggedIn');
    setIsLoggedIn(false);
    navigate('/login');
  };

  return (
    <div>
      {/* Header */}
      <header>
        <h1>CodeMax</h1>
        <nav>
          <div className="left-links">
            <Link to="/">Home</Link> |  
            <Link to="/study">Code Academy</Link> |
            <Link to="/problems">Problems</Link> | {/* Link to Problems page */}
            <Link to="/ai-assist">AI Assist</Link> {/* Link to AI Assist page */}
          </div>
          <div className="right-links">
            {isLoggedIn ? (
              <button onClick={handleLogout}>Logout</button> 
            ) : (
              <>
                <Link to="/register">Register</Link> |  
                <Link to="/login">Login</Link>
              </>
            )}
          </div>
        </nav>
      </header>

      {/* Main Routes */}
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/users" element={<Users />} />
          <Route path="/problems" element={<Problems />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} />} />
          <Route path="/verify" element={<VerifyPage />} />
          <Route path="/study" element={<Study />} />
          <Route path="/problems/:id" element={<ProblemDetails />} />
          <Route path="/ai-assist" element={<AIAssist />} /> {/* Route for AI Assist */}
        </Routes>
      </main>

      {/* Footer */}
      <footer className="about-us">
        <div className="footer-container">
          <div className="footer-column">
            <h3>About Us</h3>
            <p>
              CodeMax is a platform designed for coders to excel in their programming journey.
              From competitive coding to real-world problem-solving, we provide resources to grow your skills.
            </p>
          </div>
          <div className="footer-column">
            <h3>Contact</h3>
            <p>Email: support@codemax.com</p>
            <p>Phone: +1 123-456-7890</p>
            <p>Address: 123 CodeMax Lane, Tech City</p>
          </div>
          <div className="footer-column">
            <h3>Quick Links</h3>
            <ul>
              <li><Link to="/problems">Problems</Link></li>
              <li><Link to="/study">Code Academy</Link></li>
              <li><Link to="/register">Register</Link></li>
              <li><Link to="/login">Login</Link></li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; {new Date().getFullYear()} CodeMax. All Rights Reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default () => (
  <Router>
    <App />
  </Router>
);
