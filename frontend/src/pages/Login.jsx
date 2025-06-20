// src/pages/Login.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import './Login.css';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      // This is the original code that sends the actual login request to your backend
      const res = await axios.post('http://127.0.0.1:8000/login/', { email, password });
      
      // Assuming the backend returns the token in res.data.token
      login(res.data.token); // Store the token globally using AuthContext
      
      navigate('/'); // Redirect to the dashboard on successful login
      alert('Login successful!'); // Simple success feedback
    } catch (err) {
      console.error("Login failed:", err.response ? err.response.data : err.message);
      alert("Login failed: " + (err.response?.data?.detail || err.message)); // Provide user feedback
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={(e) => { e.preventDefault(); handleLogin(); }}>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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