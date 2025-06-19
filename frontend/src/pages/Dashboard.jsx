// src/pages/Dashboard.jsx
import React from 'react';
import WeatherCard from '../components/WeatherCard';
import AQICard from '../components/AQICard';
import PredictionCard from '../components/PredictionCard';
import DistrictSelector from '../components/DistrictSelector';
import './Dashboard.css'; // <--- NEW: Import the Dashboard's CSS

export default function Dashboard() {
  return (
    <div className="dashboard-container"> {/* <--- Using className */}
      <h1 className="dashboard-title">WeatherWave Dashboard</h1> {/* <--- Using className */}

      <DistrictSelector />

      <div className="dashboard-cards-container"> {/* <--- Using className */}
        <WeatherCard temp={25} humidity={70} />
        <AQICard aqi={120} />
        <PredictionCard prediction={28} />
      </div>
    </div>
  );
}