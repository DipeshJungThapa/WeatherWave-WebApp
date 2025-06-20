// src/hooks/useWeatherData.js
import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const useWeatherData = (latitude, longitude) => {
  const { token } = useAuth();
  const [weather, setWeather] = useState(null);
  const [aqi, setAqi] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async (lat, lon, districtName) => {
    setLoading(true);
    setError(null);

    try {
      // --- Fetch Weather Data ---
      let weatherUrl = 'http://127.0.0.1:8000/weather/';
      const weatherParams = districtName ? { district: districtName } : { lat, lon };
      const weatherHeaders = token ? { Authorization: `Bearer ${token}` } : {};

      const weatherRes = await axios.get(weatherUrl, { params: weatherParams, headers: weatherHeaders });

      // <--- NEW: Structure the weather data more comprehensively for consistency
      const fetchedWeather = {
          temp: weatherRes.data.Temp_2m,
          humidity: weatherRes.data.RH2M,
          windSpeed: weatherRes.data.WindSpeed || null, // Assume backend will provide this
          precipitation: weatherRes.data.Precipitation || null, // Assume backend will provide this
          // Add other weather fields as they become available from backend
      };
      setWeather(fetchedWeather);

      // --- Fetch AQI Data ---
      let aqiUrl = 'http://127.0.0.1:8000/aqi/';
      const aqiParams = districtName ? { district: districtName } : { lat, lon };
      const aqiHeaders = token ? { Authorization: `Bearer ${token}` } : {};

      const aqiRes = await axios.get(aqiUrl, { params: aqiParams, headers: aqiHeaders });
      setAqi(aqiRes.data.AQI_Value); // Assuming API returns AQI value directly for now

      // --- Fetch Prediction Data ---
      let predictionUrl = 'http://127.0.0.1:8000/predict/';
      const predictionParams = districtName ? { district: districtName } : { lat, lon };
      const predictionHeaders = token ? { Authorization: `Bearer ${token}` } : {};

      const predictionRes = await axios.get(predictionUrl, { params: predictionParams, headers: predictionHeaders });
      setPrediction(predictionRes.data.Predicted_Temperature); // Assuming API returns predicted temp directly for now

    } catch (err) {
      console.error("Error fetching weather data:", err);
      setError("Failed to fetch data. Please try again.");
      setWeather(null); // Clear previous data on error
      setAqi(null);
      setPrediction(null);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    if (latitude && longitude) {
      fetchData(latitude, longitude, null);
    }
  }, [latitude, longitude, fetchData]);

  return { weather, aqi, prediction, loading, error };
};

export default useWeatherData;