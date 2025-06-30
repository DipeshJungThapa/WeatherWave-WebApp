// frontend/src/hooks/useWeatherData.js
import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const useWeatherData = (latitude, longitude, district) => {
  const { token } = useAuth();
  const [weather, setWeather] = useState(null);
  const [aqi, setAqi] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [forecast, setForecast] = useState(null); // NEW: Add forecast state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async (lat, lon, districtName) => {
    setLoading(true);
    setError(null);

    try {
      let weatherUrl = 'http://127.0.0.1:8000/weather/';
      let aqiUrl = 'http://127.0.0.1:8000/aqi/';
      let predictionUrl = 'http://127.0.0.1:8000/predict_geo/';
      let forecastUrl = 'http://127.0.0.1:8000/forecast/'; // NEW: Forecast URL

      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      let params = {};
      let predictionParams = {};

      if (districtName) {
        predictionUrl = 'http://127.0.0.1:8000/predict_city/';
        predictionParams = { city: districtName };
        // For weather, AQI, and Forecast, your backend might use IP-based geolocation
        // unless you pass lat/lon explicitly, or have city-based endpoints.
        // For now, we'll keep params empty if only districtName is provided,
        // letting backend determine location for non-prediction calls.
        // If your weather/aqi/forecast APIs *can* take lat/lon even with district,
        // you'd need to convert districtName to lat/lon here or on backend.
        // For now, these will rely on backend's default behavior (e.g., IP).
        params = {}; // Keep params empty if only districtName to let backend use default
      } else if (lat && lon) {
        params = { lat, lon }; // These params will be used for GET requests
        predictionParams = { lat, lon }; // These params will be used for POST request body
      } else {
        setWeather(null);
        setAqi(null);
        setPrediction(null);
        setForecast(null); // Clear forecast too
        setLoading(false);
        setError("No location or district selected to fetch data.");
        return;
      }

      // --- Fetch Weather Data ---
      // Your backend's get_current_weather endpoint currently uses get_geolocation() from IP.
      // So, params might be ignored unless you modify that view to use them.
      const weatherRes = await axios.get(weatherUrl, { params, headers });
      const fetchedWeather = {
        temp: weatherRes.data.temp,
        humidity: weatherRes.data.humidity,
        windSpeed: weatherRes.data.wind_speed || null,
        precipitation: weatherRes.data.precip || null,
      };
      setWeather(fetchedWeather);

      // --- Fetch AQI Data ---
      // Your backend's get_aqi endpoint also uses get_geolocation().
      const aqiRes = await axios.get(aqiUrl, { params, headers });
      setAqi(aqiRes.data.AQI_Value);

      // --- Fetch Prediction Data ---
      const predictionRes = await axios.post(predictionUrl, predictionParams, { headers });
      setPrediction(predictionRes.data.predicted_temp);

      // --- NEW: Fetch 5-Day Forecast Data ---
      // Your backend's get_weather_forecast endpoint also uses get_geolocation().
      const forecastRes = await axios.get(forecastUrl, { params, headers });
      setForecast(forecastRes.data.forecast); // Assuming 'forecast' is the key holding the array

    } catch (err) {
      console.error("Error fetching data:", err); // More generic error message for all fetches
      // More specific error handling:
      if (err.response && err.response.data && err.response.data.error) {
        setError(`Error: ${err.response.data.error}`);
      } else if (err.message === "Network Error") {
        setError("Network error. Please check your internet connection and server status.");
      } else {
        setError("Failed to fetch data. Please try again.");
      }
      setWeather(null);
      setAqi(null);
      setPrediction(null);
      setForecast(null); // Clear forecast on error
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    if (district) {
      // When district is selected, lat/lon are null for primary fetch
      fetchData(null, null, district);
    } else if (latitude && longitude) {
      // Prioritize geolocation if available and no district selected
      fetchData(latitude, longitude, null);
    } else {
      setWeather(null);
      setAqi(null);
      setPrediction(null);
      setForecast(null); // Clear forecast if no location/district
      setLoading(false);
      setError(null);
    }
  }, [latitude, longitude, district, fetchData]);

  // NEW: Include forecast in the returned object
  return { weather, aqi, prediction, forecast, loading, error };
};

export default useWeatherData;