// src/components/WeatherCard.jsx
import React from 'react';
import './WeatherCard.css'; // Import the new CSS file

export default function WeatherCard({ temp, humidity }) {
  return (
    <div className="weather-card">
      <h3 className="weather-card-title">Current Weather</h3>
      <div className="weather-card-item">Temp: {temp ?? '–'}°C</div>
      <div className="weather-card-item">Humidity: {humidity ?? '–'}%</div>
    </div>
  );
}