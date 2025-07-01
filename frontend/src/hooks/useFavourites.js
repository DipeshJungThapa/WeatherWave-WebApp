// src/hooks/useFavourites.js
import { useState, useEffect, useCallback } from 'react';
import axiosInstance from '../api/axiosInstance'; // Assuming you have an axiosInstance
import { useAuth } from '../context/AuthContext';

export const useFavourites = () => {
    const [favourites, setFavourites] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { token } = useAuth(); // Get token from AuthContext

    const getAuthHeaders = useCallback(() => {
        return token ? { Authorization: `Token ${token}` } : {};
    }, [token]);

    const fetchFavourites = useCallback(async () => {
        if (!token) {
            setFavourites([]);
            setLoading(false);
            return;
        }
        setLoading(true);
        setError(null);
        try {
            const response = await axiosInstance.get('/favourite/list/', {
                headers: getAuthHeaders()
            });
            setFavourites(response.data.favourites || []);
        } catch (err) {
            console.error("Error fetching favourites:", err.response?.data || err.message);
            setError(err);
            setFavourites([]); // Clear favorites on error
        } finally {
            setLoading(false);
        }
    }, [token, getAuthHeaders]); // Depend on token and getAuthHeaders

    useEffect(() => {
        fetchFavourites();
    }, [fetchFavourites]);

    const addFavourite = async (districtName) => {
        if (!token) {
            alert("Please log in to add favorites.");
            return false;
        }
        try {
            const response = await axiosInstance.post('/favourite/add/', 
                { district: districtName }, // Send district as part of the body
                { headers: getAuthHeaders() }
            );
            console.log("Add favourite response:", response.data);
            // Re-fetch or update state locally
            fetchFavourites(); 
            return true;
        } catch (err) {
            console.error("Error adding favourite:", err.response?.data || err.message);
            setError(err);
            alert(`Failed to add favorite: ${err.response?.data?.message || err.response?.data?.error || err.message}`);
            return false;
        }
    };

    const removeFavourite = async (districtName) => {
        if (!token) {
            alert("Please log in to remove favorites.");
            return false;
        }
        try {
            // IMPORTANT: For DELETE with body, data property is used
            const response = await axiosInstance.delete('/favourite/remove/', {
                data: { district: districtName }, // Send district in data for DELETE
                headers: getAuthHeaders()
            });
            console.log("Remove favourite response:", response.data);
            // Re-fetch or update state locally
            fetchFavourites(); 
            return true;
        } catch (err) {
            console.error("Error removing favourite:", err.response?.data || err.message);
            setError(err);
            alert(`Failed to remove favorite: ${err.response?.data?.message || err.response?.data?.error || err.message}`);
            return false;
        }
    };

    return { favourites, loading, error, addFavourite, removeFavourite, fetchFavourites };
};