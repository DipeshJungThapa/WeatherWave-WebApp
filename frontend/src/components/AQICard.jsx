// frontend/src/components/AQICard.jsx
import React from 'react';
import './AQICard.css'; // Assuming you have a CSS file for this card

function AQICard({ aqi }) {
  // Check if aqi is a valid number before attempting to display it
  const displayAqi = aqi !== null && aqi !== undefined && !isNaN(aqi) ? aqi : 'N/A';

  return (
    <div className="aqi-card card">
      <h3>Air Quality Index</h3>
      <p>Overall AQI: {displayAqi}</p> {/* Only display the overall AQI */}
    </div>
  );
}

export default AQICard;