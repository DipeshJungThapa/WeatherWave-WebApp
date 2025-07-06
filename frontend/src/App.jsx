// frontend/src/App.jsx

import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, Navigate } from 'react-router-dom';
import { ThemeProvider } from 'next-themes';
import Dashboard from './pages/Dashboard';
import AuthPage from './pages/AuthPage';
import ProfilePage from './pages/ProfilePage';
import FavoriteLocations from './components/FavoriteLocations';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';

// PrivateRoute component to protect routes
function PrivateRoute({ children }) {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

function AppContent() {
  const { user } = useAuth();
  const [currentDistrict, setCurrentDistrict] = useState('Kathmandu'); // Or your default city
  const [unit, setUnit] = useState('Celsius'); // Added unit state
  const navigate = useNavigate();

  // This function is crucial for updating the Dashboard when a favorite is selected
  const handleSelectFavoriteFromList = (cityName) => {
    setCurrentDistrict(cityName);
    navigate('/dashboard'); // Navigate to dashboard after selecting favorite
  };

  const handleFavoriteRemoved = (removedCityName) => {
    console.log(`Favorite ${removedCityName} was removed. Re-evaluating dashboard favorite status.`);
    // You might want to trigger a refresh or re-fetch favorites here if needed
  };

  const toggleUnit = () => {
    setUnit((prevUnit) => (prevUnit === 'Celsius' ? 'Fahrenheit' : 'Celsius'));
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar
        onLocationChange={setCurrentDistrict}
        currentDistrict={currentDistrict}
        user={user}
        unit={unit}
        toggleUnit={toggleUnit}
      />
      <main className="flex-1 p-4">
        <Routes>
          <Route
            path="/"
            element={
              <PrivateRoute>
                <Dashboard currentDistrict={currentDistrict} unit={unit} />
              </PrivateRoute>
            }
          />
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard currentDistrict={currentDistrict} unit={unit} />
              </PrivateRoute>
            }
          />
          <Route path="/login" element={<AuthPage mode="login" />} />
          <Route path="/register" element={<AuthPage mode="register" />} />
          <Route
            path="/profile"
            element={
              <PrivateRoute>
                <ProfilePage user={user} />
              </PrivateRoute>
            }
          />
          <Route
            path="/favorites"
            element={
              <PrivateRoute>
                <div className="container mx-auto p-4 max-w-2xl">
                  <FavoriteLocations
                    onSelectFavorite={handleSelectFavoriteFromList}
                    onFavoriteRemoved={handleFavoriteRemoved}
                  />
                </div>
              </PrivateRoute>
            }
          />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <ThemeProvider attribute="class">
          <AppContent />
        </ThemeProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;
