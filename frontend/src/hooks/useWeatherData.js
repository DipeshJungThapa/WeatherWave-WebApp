// frontend/src/hooks/useWeatherData.js
import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext'; // Assuming useAuth is used for token

const useWeatherData = (latitude, longitude, district) => { // ADDED DISTRICT HERE
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
      let weatherUrl = 'http://127.0.0.1:8000/weather/';
      let aqiUrl = 'http://127.0.0.1:8000/aqi/';
      let predictionUrl = 'http://127.0.0.1:8000/predict/';

      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      let params = {};

      if (districtName) {
        params = { district: districtName };
      } else if (lat && lon) {
        params = { lat, lon };
      } else {
        // If no criteria, clear data and return
        setWeather(null);
        setAqi(null);
        setPrediction(null);
        setLoading(false);
        setError("No location or district selected to fetch data.");
        return;
      }

      // --- Fetch Weather Data ---
      const weatherRes = await axios.get(weatherUrl, { params, headers });
      const fetchedWeather = {
        temp: weatherRes.data.Temp_2m,
        humidity: weatherRes.data.RH2M,
        windSpeed: weatherRes.data.WindSpeed || null,
        precipitation: weatherRes.data.Precipitation || null,
      };
      setWeather(fetchedWeather);

      // --- Fetch AQI Data ---
      const aqiRes = await axios.get(aqiUrl, { params, headers });
      setAqi(aqiRes.data.AQI_Value);

      // --- Fetch Prediction Data ---
      const predictionRes = await axios.get(predictionUrl, { params, headers });
      setPrediction(predictionRes.data.Predicted_Temperature);

    } catch (err) {
      console.error("Error fetching weather data:", err);
      setError("Failed to fetch data. Please try again.");
      setWeather(null);
      setAqi(null);
      setPrediction(null);
    } finally {
      setLoading(false);
    }
  }, [token]); // Dependencies for useCallback: only token if it affects the request directly

  useEffect(() => {
    // Trigger fetch if latitude/longitude or district changes
    if (latitude && longitude) {
      fetchData(latitude, longitude, null); // Prioritize geolocation
    } else if (district) {
      fetchData(null, null, district); // Fallback to district
    } else {
      // If neither, clear data
      setWeather(null);
      setAqi(null);
      setPrediction(null);
      setLoading(false);
      setError(null);
    }
  }, [latitude, longitude, district, fetchData]); // ADDED DISTRICT HERE AND fetchData

  return { weather, aqi, prediction, loading, error };
};

export default useWeatherData;