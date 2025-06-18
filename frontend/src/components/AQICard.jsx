// src/components/AQICard.jsx
import React from 'react';
import './AQICard.css'; // Import the new CSS file

export default function AQICard({ aqi }) {
  return (
    <div className="aqi-card">
      <h3 className="aqi-card-title">Air Quality Index</h3>
      <div className="aqi-card-item">AQI: {aqi ?? '–'}</div>
    </div>
  );
}