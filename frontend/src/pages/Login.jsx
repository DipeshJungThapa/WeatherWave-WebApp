// src/pages/Login.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import "./Login.css";

export default function Login() {
  const [username, setUsername] = useState(''); // Change email to username state
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      // Change the field name from 'email' to 'username' in the payload
      const res = await axios.post('http://127.0.0.1:8000/login/', { username, password });
      
      login(res.data.token); 
      
      navigate('/'); 
      alert('Login successful!');
    } catch (err) {
      console.error("Login failed:", err.response ? err.response.data : err.message);
      // It's good to show specific error messages from the backend
      const errorMessage = err.response?.data?.error || err.response?.data?.detail || err.message;
      alert("Login failed: " + errorMessage);
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={(e) => { e.preventDefault(); handleLogin(); }}>
        <div className="form-group">
          {/* Change label and state/onChange to username */}
          <label htmlFor="username">Username:</label>
          <input
            type="text" // Changed type to text, as username might not be an email format
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}