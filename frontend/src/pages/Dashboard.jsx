// src/pages/Dashboard.jsx
import React, { useState } from 'react'; // We need useState for the DistrictSelector
import WeatherCard from '../components/WeatherCard';
import AQICard from '../components/AQICard';
import PredictionCard from '../components/PredictionCard';
import DistrictSelector from '../components/DistrictSelector';

export default function Dashboard() {
  const [selectedDistrict, setSelectedDistrict] = useState('Kathmandu'); // Default district for the selector

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column', // Stack items vertically
      alignItems: 'center',    // Center horizontally
      minHeight: '100vh',      // Take full viewport height
      padding: '20px',
      boxSizing: 'border-box',
      backgroundColor: '#1a1a1a' // Ensure background is dark for this page as well
    }}>
      <h1 style={{ color: 'white', marginBottom: '20px' }}>WeatherWave Dashboard</h1>

      {/* District Selector */}
      <DistrictSelector
        district={selectedDistrict}
        onChange={setSelectedDistrict}
      />

      {/* Container for the Weather Cards */}
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',     // Allow cards to wrap to the next line on smaller screens
        justifyContent: 'center', // Center cards horizontally within this container
        gap: '20px',          // Space between the cards
        marginTop: '20px'
      }}>
        <WeatherCard temp={25} humidity={70} /> {/* Displaying dummy data for the stub */}
        <AQICard aqi={120} />                   {/* Displaying dummy data for the stub */}
        <PredictionCard prediction={28} />      {/* Displaying dummy data for the stub */}
      </div>
    </div>
  );
}