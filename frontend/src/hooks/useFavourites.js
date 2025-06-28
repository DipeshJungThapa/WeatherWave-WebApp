// src/hooks/useFavourites.js
import { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext'; // To get the auth token

const useFavourites = () => {
  const { token } = useAuth(); // Get the authentication token
  const [favorites, setFavorites] = useState([]); // State to store the list of favorite districts
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Function to fetch favorites from the backend
  const fetchFavorites = async () => {
    if (!token) {
      setFavorites([]); // Clear favorites if no token
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const headers = { Authorization: `Token ${token}` };
      // This will call your future backend endpoint for fetching favorites
      const res = await axios.get('/favourite/list/', { headers }); // Assuming /favourite/list/ endpoint
      setFavorites(res.data.favorites || []); // Assuming response has a 'favorites' key
    } catch (err) {
      console.error("Error fetching favorites:", err);
      setError('Failed to load favorites.');
      setFavorites([]);
    } finally {
      setLoading(false);
    }
  };

  // Function to add a district to favorites
  const addFavorite = async (districtName) => {
    if (!token) {
      setError('Login required to add favorites.');
      return;
    }
    try {
      const headers = { Authorization: `Token ${token}` };
      // This will call your future backend endpoint for adding a favorite
      await axios.post('/favourite/add/', { district: districtName }, { headers }); // Assuming /favourite/add/ endpoint
      // After successful addition, refetch the list to update UI
      await fetchFavorites();
    } catch (err) {
      console.error("Error adding favorite:", err);
      setError('Failed to add favorite.');
    }
  };

  // Function to remove a district from favorites
  const removeFavorite = async (districtName) => {
    if (!token) {
      setError('Login required to remove favorites.');
      return;
    }
    try {
      const headers = { Authorization: `Token ${token}` };
      // This will call your future backend endpoint for removing a favorite
      // Assuming DELETE or POST with identifier for removal
      await axios.post('/favourite/remove/', { district: districtName }, { headers }); // Assuming /favourite/remove/ endpoint
      // After successful removal, refetch the list to update UI
      await fetchFavorites();
    } catch (err) {
      console.error("Error removing favorite:", err);
      setError('Failed to remove favorite.');
    }
  };

  // Fetch favorites when the component mounts or token changes
  useEffect(() => {
    fetchFavorites();
  }, [token]); // Re-fetch if token changes (e.g., user logs in/out)

  // Return favorite data and functions
  return { favorites, loading, error, addFavorite, removeFavorite, fetchFavorites };
};

export default useFavourites;