// frontend/src/services/authService.js
import axios from 'axios';

// Define specific URLs for authentication and favorites
const REGISTER_URL = 'http://127.0.0.1:8000/register/';
const LOGIN_URL = 'http://127.0.0.1:8000/login/';
const USERS_URL = 'http://127.0.0.1:8000/users/';
const FAVORITES_API_URL = 'http://127.0.0.1:8000/api/favorites/';

// Update register function to use specific URL
const register = async (userData) => {
    try {
        const response = await axios.post(REGISTER_URL, userData);
        return response.data; // Returns { message: "User created successfully", user_id: user.id }
    } catch (error) {
        console.error("Registration error:", error.response?.data || error.message);
        throw error;
    }
};

// Update login function to use specific URL
const login = async (username, password) => {
    try {
        const response = await axios.post(LOGIN_URL, { username, password });
        return response.data; // Returns { message, user, token }
    } catch (error) {
        console.error("Login error:", error.response?.data || error.message);
        throw error;
    }
};

// Logout a user
// Requires the authentication token in the headers
const logout = async (token) => {
    try {
        const response = await axios.post(
            `${API_URL}logout/`,
            {}, // Empty body for POST request
            {
                headers: {
                    'Authorization': `Token ${token}`
                }
            }
        );
        return response.data; // Returns confirmation message
    } catch (error) {
        console.error("Logout error:", error.response?.data || error.message);
        throw error;
    }
};

// Favorites API remains unchanged
const fetchFavorites = async (token) => {
    const response = await fetch(FAVORITES_API_URL, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`,
        },
    });
    if (!response.ok) {
        throw new Error(`Fetching favorites failed: ${response.statusText}`);
    }
    return await response.json();
};

const authService = {
    register,
    login,
    logout,
    fetchFavorites,
};

export default authService;