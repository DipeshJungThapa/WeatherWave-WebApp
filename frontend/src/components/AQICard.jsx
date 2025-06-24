// src/components/AQICard.jsx
import React from 'react';
import './AQICard.css'; // Make sure this CSS file exists

export default function AQICard({ aqi }) {
  // Assuming 'aqi' prop will be an object like { overall: ..., pm25: ..., pm10: ..., recommendation: ... }
  // Default to N/A if properties are missing
  const overallAqi = aqi?.overall ?? 'N/A';
  const pm25 = aqi?.pm25 ?? 'N/A';
  const pm10 = aqi?.pm10 ?? 'N/A';
  const recommendation = aqi?.recommendation ?? 'No specific recommendation available.';

  // Function to determine color based on AQI value (example logic, adjust as needed)
  const getAqiColor = (value) => {
    if (value === 'N/A') return '#999'; // Gray for N/A
    if (value <= 50) return '#00b050'; // Green: Good
    if (value <= 100) return '#92d050'; // Light Green: Moderate
    if (value <= 150) return '#ffff00'; // Yellow: Unhealthy for Sensitive Groups
    if (value <= 200) return '#ffc000'; // Orange: Unhealthy
    if (value <= 300) return '#ff0000'; // Red: Very Unhealthy
    return '#c00000'; // Dark Red: Hazardous
  };

  return (
    <div className="aqi-card">
      <h2 className="card-title">Air Quality Index</h2>
      <div className="card-content">
        <div className="aqi-overall">
          <p className="aqi-label">Overall AQI:</p>
          <p className="aqi-value" style={{ color: getAqiColor(overallAqi) }}>
            {overallAqi}
          </p>
        </div>

        <div className="aqi-pollutants">
          <p className="pollutant-item">PM2.5: {pm25} µg/m³</p>
          <p className="pollutant-item">PM10: {pm10} µg/m³</p>
        </div>

        <div className="aqi-recommendation">
          <h3 className="recommendation-title">Health Recommendation:</h3>
          <p className="recommendation-text">{recommendation}</p>
        </div>
      </div>
    </div>
  );
}