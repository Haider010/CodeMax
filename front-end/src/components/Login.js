import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // useNavigate for redirection
import axios from 'axios';
import './styles/Login.css'; // Import the CSS file for styling

const Login = ({ setIsLoggedIn }) => { // Receive setIsLoggedIn as a prop
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [message, setMessage] = useState('');
  const navigate = useNavigate(); // Hook to navigate to the Home page

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/login', formData);

      // Check if the status code is 200 before marking as logged in
      if (response.status === 200 ) {
        setMessage(response.data.message);
        localStorage.setItem('userLoggedIn', 'true'); // Store logged-in state in localStorage
        setIsLoggedIn(true); // Update logged-in state in App
        navigate('/'); // Redirect to Home page
      } else {
        setMessage('Login failed. Please check your credentials.');
      }
    } catch (error) {
      setMessage(error.response?.data?.error || 'An error occurred');
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="email"
              name="email"
              placeholder="Enter your email"
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <input
              type="password"
              name="password"
              placeholder="Enter your password"
              onChange={handleChange}
              required
            />
          </div>
          <button type="submit" className="login-button">
            Login
          </button>
        </form>
        {message && <p className="message">{message}</p>}
        <p className="register-link">
          Don’t have an account? <Link to="/register">Register here</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
