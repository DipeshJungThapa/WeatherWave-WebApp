// src/App.jsx
import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import AuthPage from './pages/AuthPage';
import { ThemeProvider } from './components/theme-provider'; // Import ThemeProvider

function App() {
  return (
    // BrowserRouter must be the outermost component for routing to work correctly
    <BrowserRouter>
      {/* ThemeProvider wraps the rest of the app to provide theme context */}
      <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
        {/* This div sets up the main flex column layout for Navbar, Main content, and Footer */}
        <div className="flex flex-col min-h-screen bg-background text-foreground">
          <Navbar /> {/* Navbar is always visible */}
          {/* Main content area, takes up remaining vertical space */}
          <main className="flex-1">
            {/* Routes define which component to render based on the URL path */}
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/auth" element={<AuthPage />} />
              {/* Add more routes here as your application grows */}
            </Routes>
          </main>
          {/* Global Footer, sticks to the bottom */}
          <footer className="bg-popover text-popover-foreground p-4 text-center shadow-inner">
            <p>&copy; {new Date().getFullYear()} WeatherWave. All rights reserved.</p>
          </footer>
        </div>
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;