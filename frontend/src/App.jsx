// src/App.jsx
import React from 'react';
import { Routes, Route, Link, useNavigate } from 'react-router-dom'; // <--- NEW: Link, useNavigate
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import { useAuth } from './context/AuthContext'; // <--- NEW: useAuth hook

function App() {
  const { token, logout } = useAuth(); // Get token and logout function
  const navigate = useNavigate(); // For redirection after logout

  const handleLogout = () => {
    logout(); // Clear token from state and localStorage
    navigate('/login'); // Redirect to login page
    alert('Logged out successfully!');
  };

  return (
    <div className="App">
      <nav style={{ 
        backgroundColor: '#333', 
        padding: '10px 20px', 
        marginBottom: '20px',
        display: 'flex',
        justifyContent: 'flex-end', /* Align items to the right */
        alignItems: 'center',
        gap: '15px'
      }}>
        {token ? (
          <button
            onClick={handleLogout}
            style={{
              backgroundColor: '#dc3545', /* Red for logout */
              color: 'white',
              padding: '8px 12px',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
              fontSize: '0.9em',
              transition: 'background-color 0.2s ease',
            }}
          >
            Logout
          </button>
        ) : (
          <Link to="/login" style={{ color: 'white', textDecoration: 'none', fontSize: '1em' }}>
            Login
          </Link>
        )}
      </nav>

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/login" element={<Login />} />
        {/* Add more routes here as needed */}
      </Routes>
    </div>
  );
}

export default App;