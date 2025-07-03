// frontend/src/context/AuthContext.jsx
import React, { createContext, useState, useEffect, useContext } from 'react';
// Make sure this path is correct, should be authService.js
import authService from '../services/authApi'; // Corrected import to match the file name

// Create the AuthContext
const AuthContext = createContext(null);

// Custom hook to use the AuthContext
export const useAuth = () => {
    return useContext(AuthContext);
};

// AuthProvider component to wrap your application
export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(null);
    const [loading, setLoading] = useState(true);

    // Effect to check for stored token/user on initial load
    useEffect(() => {
        const storedToken = localStorage.getItem('token');
        const storedUser = localStorage.getItem('user');

        if (storedToken && storedUser) {
            try {
                setUser(JSON.parse(storedUser));
                setToken(storedToken);
                setIsAuthenticated(true);
            } catch (error) {
                console.error("Failed to parse stored user data:", error);
                localStorage.removeItem('token');
                localStorage.removeItem('user');
            }
        }
        setLoading(false);
    }, []);

    // Login function
    const login = async (username, password) => {
        try {
            const data = await authService.login(username, password); // Use authService
            setToken(data.token);
            setUser(data.user);
            setIsAuthenticated(true);
            // --- Crucial: Explicitly save token and user to localStorage here ---
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            // --- END Crucial ---
            return data;
        } catch (error) {
            setIsAuthenticated(false);
            setUser(null);
            setToken(null);
            // --- Crucial: Also clear localStorage on failed login attempt ---
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            // --- END Crucial ---
            console.error("Login failed in AuthContext:", error);
            throw error;
        }
    };

    // Register function
    const register = async (userData) => {
        try {
            const data = await authService.register(userData); // Use authService
            return data;
        } catch (error) {
            console.error("Registration failed in AuthContext:", error);
            throw error;
        }
    };

    // Logout function
    const logout = async () => {
        try {
            await authService.logout(token); // Use authService
        } catch (error) {
            console.error("Logout API call failed:", error);
        } finally {
            setIsAuthenticated(false);
            setUser(null);
            setToken(null);
            // --- Crucial: Explicitly clear token and user from localStorage on logout ---
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            // --- END Crucial ---
        }
    };

    const authContextValue = {
        isAuthenticated,
        user,
        token,
        loading,
        login,
        register,
        logout,
    };

    return (
        <AuthContext.Provider value={authContextValue}>
            {!loading && children}
        </AuthContext.Provider>
    );
};