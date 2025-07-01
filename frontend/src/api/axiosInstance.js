// frontend/src/api/axiosInstance.js
import axios from 'axios';

// IMPORTANT: Ensure VITE_BACKEND_URL is set in your .env file in the frontend root
// Example: VITE_BACKEND_URL=http://127.0.0.1:8000
const BACKEND_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000';

const axiosInstance = axios.create({
    baseURL: `${BACKEND_BASE_URL}/`, // Ensure this ends with a slash if your Django urls.py has app-level prefixes like /api/
    timeout: 5000, // Request will timeout after 5 seconds
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
});

// Add a request interceptor to include the authentication token automatically
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token'); // Assuming you store the token in localStorage
        if (token) {
            // Use 'Token ' prefix as required by Django REST Framework's TokenAuthentication
            config.headers.Authorization = `Token ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default axiosInstance;