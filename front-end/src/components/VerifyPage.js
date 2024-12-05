import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/VerifyPage.css';

const VerifyPage = () => {
  const [formData, setFormData] = useState({ email: '', verificationCode: '' });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (message) {
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    }
  }, [message, navigate]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = {
      email: formData.email,
      code: formData.verificationCode,
    };

    fetch('http://localhost:5000/verify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message) {
          setMessage(data.message);
          setError('');
        } else {
          setError(data.error || 'An error occurred');
          setMessage('');
        }
      })
      .catch(() => setError('Verification failed. Please try again.'));
  };

  return (
    <div className="verify-container">
      <div className="verify-box">
        <h2>Verify Your Email</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="email"
              name="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <input
              type="text"
              name="verificationCode"
              placeholder="Enter your verification code"
              value={formData.verificationCode}
              onChange={handleChange}
              required
            />
          </div>
          <button type="submit" className="verify-button">
            Verify
          </button>
        </form>
        {message && <p className="message">{message}</p>}
        {error && <p className="error">{error}</p>}
      </div>
    </div>
  );
};

export default VerifyPage;
