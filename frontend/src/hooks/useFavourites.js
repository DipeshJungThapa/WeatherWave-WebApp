// src/hooks/useFavourites.js
import { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  headers: {
    'Content-Type': 'application/json',
  },
});

const useFavourites = () => {
  const { token } = useAuth();
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const getAuthHeaders = () => ({
    Authorization: `Token ${token}`,
  });

  const fetchFavorites = async () => {
    if (!token) {
      setFavorites([]);
      setLoading(false);
      return;
    }

    setLoading(true);
    try {
      const res = await axiosInstance.get('/favourite/list/', {
        headers: getAuthHeaders(),
      });
      setFavorites(res.data.favourites || []);
    } catch (err) {
      console.error('Error fetching favorites:', err);
      setError('Failed to load favorites.');
      setFavorites([]);
    } finally {
      setLoading(false);
    }
  };

  const addFavorite = async (districtName) => {
    if (!token) {
      alert('Please log in to add favorites.');
      return;
    }

    try {
      const res = await axiosInstance.post(
        '/favourite/add/',
        { district: districtName }, // <-- FIXED HERE
        { headers: getAuthHeaders() }
      );
      if (res.status === 201 || res.status === 200) {
        alert(`'${districtName}' added to favorites!`);
        await fetchFavorites();
      } else {
        alert('Something went wrong while adding favorite.');
      }
    } catch (err) {
      console.error('Add favorite error:', err);
      alert(err.response?.data?.detail || 'Failed to add favorite.');
    }
  };

  const removeFavorite = async (districtName) => {
    if (!token) {
      alert('Please log in to remove favorites.');
      return;
    }

    try {
      const res = await axiosInstance.post(
        '/favourite/remove/',
        { district: districtName }, // <-- FIXED HERE
        { headers: getAuthHeaders() }
      );
      if (res.status === 200) {
        alert(`'${districtName}' removed from favorites!`);
        await fetchFavorites();
      } else {
        alert('Something went wrong while removing favorite.');
      }
    } catch (err) {
      console.error('Remove favorite error:', err);
      alert(err.response?.data?.detail || 'Failed to remove favorite.');
    }
  };

  useEffect(() => {
    fetchFavorites();
  }, [token]);

  return {
    favorites,
    loading,
    error,
    addFavorite,
    removeFavorite,
    fetchFavorites,
  };
};

export default useFavourites;
