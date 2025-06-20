// src/pages/Dashboard.jsx
import React, { useEffect } from 'react'; // <--- NEW: useEffect imported here
import './Dashboard.css';
import DistrictSelector from '../components/DistrictSelector';
import WeatherCard from '../components/WeatherCard';
import AQICard from '../components/AQICard';
import PredictionCard from '../components/PredictionCard';
import useWeatherData from '../hooks/useWeatherData';
import useGeolocation from '../hooks/useGeolocation'; // <--- NEW IMPORT: Our geolocation hook
import { useDistrict } from '../context/DistrictContext'; // <--- NEW IMPORT: To get selectedDistrict

export default function Dashboard() {
  const { weather, aqi, prediction, loading, error } = useWeatherData();
  const { location, permissionDenied } = useGeolocation(); // <--- NEW: Use geolocation hook
  const { district } = useDistrict(); // <--- NEW: Get district from context for logging

  // <--- NEW: Log location or district for verification
  useEffect(() => {
    if (location) {
      console.log("Geolocation: User location obtained:", location);
      // Later, we'll use this location for API calls if available
    } else if (permissionDenied) {
      console.log("Geolocation: Permission denied or not supported. Falling back to selected district.");
    } else if (district) {
      // This will be logged if location is not available and not explicitly denied (e.g. still prompting or error)
      // or as a fallback
      console.log("Using selected district for now:", district);
    }
  }, [location, permissionDenied, district]); // Re-run when these values change

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">WeatherWave Dashboard</h1>

      <DistrictSelector />

      <div className="dashboard-cards-container">
        {loading && <p style={{ color: 'white' }}>Loading data for {district}...</p>}
        {error && <p style={{ color: 'red' }}>Error: {error}. Please try again.</p>}

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