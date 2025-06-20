// src/pages/Dashboard.jsx
import React, { useEffect } from 'react';
import './Dashboard.css';
import DistrictSelector from '../components/DistrictSelector';
import WeatherCard from '../components/WeatherCard';
import AQICard from '../components/AQICard';
import PredictionCard from '../components/PredictionCard';
import useWeatherData from '../hooks/useWeatherData';
import useGeolocation from '../hooks/useGeolocation';
import { useDistrict } from '../context/DistrictContext';

export default function Dashboard() {
  // Get location data from useGeolocation hook
  const { location, permissionDenied } = useGeolocation();
  // Extract latitude and longitude if location is available, otherwise null
  const latitude = location ? location.lat : null;
  const longitude = location ? location.lon : null;

  // Get district from context
  const { district } = useDistrict();

  // Pass latitude, longitude, and district to useWeatherData
  // The useWeatherData hook will now decide whether to use lat/lon or district
  const { weather, aqi, prediction, loading, error } = useWeatherData(latitude, longitude);

  // Effect for logging which location source is being used (for verification)
  useEffect(() => {
    if (latitude && longitude) {
      console.log("Dashboard: Data will be fetched using Geolocation coordinates:", { latitude, longitude });
    } else if (permissionDenied) {
      console.log("Dashboard: Geolocation permission denied. Data will be fetched using selected district:", district);
    } else {
      // This will primarily log when location is not yet available, or falls back to district initially
      console.log("Dashboard: Geolocation not available or pending. Data will be fetched using selected district:", district);
    }
  }, [latitude, longitude, permissionDenied, district]); // Dependencies

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">WeatherWave Dashboard</h1>

      <DistrictSelector />

      <div className="dashboard-cards-container">
        {/* Display loading, error, or data based on the useWeatherData hook */}
        {loading && <p style={{ color: 'white' }}>Loading data...</p>}
        {error && <p style={{ color: 'red' }}>Error: {error}</p>}

        {!loading && weather && (
          <>
            <WeatherCard temp={weather.Temp_2m} humidity={weather.RH2M} />
            <AQICard aqi={aqi ?? 'N/A'} />
            <PredictionCard prediction={prediction ?? 'N/A'} />
          </>
        )}

        {!loading && !error && !weather && (
          <p style={{ color: 'gray' }}>Select a district to fetch data.</p>
        )}
      </div>
    </div>
  );
}