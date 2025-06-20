// src/pages/Dashboard.jsx
import React from 'react';
import './Dashboard.css'; // Keep existing CSS import
import DistrictSelector from '../components/DistrictSelector';
import WeatherCard from '../components/WeatherCard';
import AQICard from '../components/AQICard';
import PredictionCard from '../components/PredictionCard';
import useWeatherData from '../hooks/useWeatherData'; // <--- NEW IMPORT: Our custom hook

export default function Dashboard() {
  // <--- NEW: Use the custom hook to get data, loading status, and error
  const { weather, aqi, prediction, loading, error } = useWeatherData();

  return (
    <div className="dashboard-container"> {/* Using existing class name */}
      <h1 className="dashboard-title">WeatherWave Dashboard</h1> {/* Using existing class name */}

      <DistrictSelector />

      <div className="dashboard-cards-container"> {/* Using existing class name */}
        {/* <--- NEW: Conditional rendering based on loading/error/data */}
        {loading && <p style={{ color: 'white' }}>Loading data for {error ? '' : 'selected district'}...</p>}
        {error && <p style={{ color: 'red' }}>Error: {error}. Please try again.</p>}

        {/* Render cards only if not loading and data is available */}
        {!loading && weather && (
          <>
            <WeatherCard temp={weather.Temp_2m} humidity={weather.RH2M} />
            <AQICard aqi={aqi ?? 'N/A'} /> {/* Use 'N/A' if AQI is null or undefined */}
            <PredictionCard prediction={prediction ?? 'N/A'} /> {/* Use 'N/A' if prediction is null or undefined */}
          </>
        )}

        {/* Optional: If no data and not loading/error, maybe show a prompt */}
        {!loading && !error && !weather && (
          <p style={{ color: 'gray' }}>Select a district to fetch data.</p>
        )}

      </div>
    </div>
  );
}