// src/context/PreferencesContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';

// 1. Create the Context
const PreferencesContext = createContext();

// 2. Create a custom hook to use the context easily
export const usePreferences = () => {
  return useContext(PreferencesContext);
};

// 3. Create the Provider Component
export const PreferencesProvider = ({ children }) => {
  // Initialize state from localStorage or set default values
  const [tempUnit, setTempUnit] = useState(() => {
    return localStorage.getItem('tempUnit') || 'C'; // Default to Celsius
  });

  const [windUnit, setWindUnit] = useState(() => {
    return localStorage.getItem('windUnit') || 'ms'; // Default to meters/second
  });

  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || 'dark'; // Default to dark mode
  });

  // Update localStorage whenever preferences change
  useEffect(() => {
    localStorage.setItem('tempUnit', tempUnit);
  }, [tempUnit]);

  useEffect(() => {
    localStorage.setItem('windUnit', windUnit);
  }, [windUnit]);

  useEffect(() => {
    localStorage.setItem('theme', theme);
    // You might want to apply the theme to the body or root element here
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  // Initial theme application when component mounts
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, []); // Empty dependency array means this runs once on mount

  // Value provided by the context
  const value = {
    tempUnit,
    setTempUnit,
    windUnit,
    setWindUnit,
    theme,
    setTheme,
  };

  return (
    <PreferencesContext.Provider value={value}>
      {children}
    </PreferencesContext.Provider>
  );
};