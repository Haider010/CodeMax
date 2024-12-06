import React, { useState } from 'react';
import './styles/AIAssist.css';

const AIAssist = () => {
  const [userInput, setUserInput] = useState('');
  const [messages, setMessages] = useState([
    { sender: 'AI', text: 'Hello! How can I assist you today?' },
  ]);

  const isLoggedIn = localStorage.getItem('userLoggedIn') === 'true'; // Check login status from localStorage

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isLoggedIn) {
      alert('You need to log in to send a message!');
      return;
    }

    if (userInput.trim() !== '') {
      const updatedMessages = [
        ...messages,
        { sender: 'User', text: userInput },
      ];
      setMessages(updatedMessages);

      try {
        // Make POST request to Flask backend
        const response = await fetch('http://127.0.0.1:5000/api/get-response', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: userInput,
            conversation_history: updatedMessages
              .filter((msg) => msg.sender === 'User')
              .map((msg) => msg.text),
          }),
        });

        const data = await response.json();

        if (data.success) {
          setMessages([
            ...updatedMessages,
            { sender: 'AI', text: data.reply },
          ]);
        } else {
          setMessages([
            ...updatedMessages,
            { sender: 'AI', text: 'Sorry, there was an error processing your request.' },
          ]);
        }
      } catch (error) {
        setMessages([
          ...updatedMessages,
          { sender: 'AI', text: 'Sorry, something went wrong.' },
        ]);
      }

      setUserInput('');
    }
  };

  return (
    <div className="ai-assist">
      <h2>AI Assist</h2>
      <div className="chat-box">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender.toLowerCase()}`}>
            <span>{message.sender}:</span>
            <p>{message.text}</p>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default AIAssist;
