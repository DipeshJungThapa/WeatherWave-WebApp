// frontend/src/App.jsx

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom'; // <--- ADDED useNavigate
import Dashboard from './pages/Dashboard';
import AuthPage from './pages/AuthPage';
import ProfilePage from './pages/ProfilePage';
import FavoriteLocations from './components/FavoriteLocations';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';

function AppContent() {
    const { isAuthenticated, user, logout } = useAuth();
    const [currentDistrict, setCurrentDistrict] = useState('Kathmandu'); // Or your default city
    const navigate = useNavigate(); // <--- INITIALIZE useNavigate HERE

    // This function is crucial for updating the Dashboard when a favorite is selected
    const handleSelectFavoriteFromList = (cityName) => {
        setCurrentDistrict(cityName);
        // NEW: Navigate to the dashboard after selecting a favorite
        navigate('/dashboard'); // <--- ADDED NAVIGATION
    };

    const handleFavoriteRemoved = (removedCityName) => {
        console.log(`Favorite ${removedCityName} was removed. Re-evaluating dashboard favorite status.`);
        // You might want to re-fetch favorites here or trigger a refresh in FavoriteLocations
        // if its internal state isn't already reactive to deletions.
    };

    return (
        <div className="flex flex-col min-h-screen">
            <Navbar onLocationChange={setCurrentDistrict} currentDistrict={currentDistrict} user={user} />
            <main className="flex-1 p-4">
                <Routes>
                    <Route path="/" element={<Dashboard currentDistrict={currentDistrict} />} />
                    <Route path="/dashboard" element={<Dashboard currentDistrict={currentDistrict} />} />

                    <Route path="/login" element={<AuthPage mode="login" />} />
                    <Route path="/register" element={<AuthPage mode="register" />} />

                    <Route
                        path="/profile"
                        element={<ProfilePage user={user} />}
                    />

                    {/* Dedicated route for FavoriteLocations */}
                    <Route
                        path="/favorites"
                        element={
                            <div className="container mx-auto p-4 max-w-2xl">
                                <FavoriteLocations
                                    onSelectFavorite={handleSelectFavoriteFromList}
                                    onFavoriteRemoved={handleFavoriteRemoved}
                                />
                            </div>
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
                <AppContent />
            </AuthProvider>
        </Router>
    );
}

export default App;