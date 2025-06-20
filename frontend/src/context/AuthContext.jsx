// src/context/AuthContext.jsx
import { createContext, useContext, useState } from 'react';

// Create the AuthContext
const AuthContext = createContext();

// AuthProvider component to wrap your app and provide authentication state
export function AuthProvider({ children }) {
  // Initialize token state from localStorage, or null if not found
  const [token, setToken] = useState(localStorage.getItem('token') || null);

  // Function to handle user login: set token in state and localStorage
  const login = (newToken) => { // Renamed param to newToken to avoid conflict with state variable
    setToken(newToken);
    localStorage.setItem('token', newToken);
  };

  // Function to handle user logout: clear token from state and localStorage
  const logout = () => {
    setToken(null);
    localStorage.removeItem('token');
  };

  // The value provided to children includes the token and login/logout functions
  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook to easily consume the AuthContext in any component
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};