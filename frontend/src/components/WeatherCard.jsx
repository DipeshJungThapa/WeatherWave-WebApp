// src/components/WeatherCard.jsx
import React from 'react';
import './WeatherCard.css';
import { usePreferences } from '../context/PreferencesContext';

// <--- NEW: Added windSpeed and precipitation props
export default function WeatherCard({ temp, humidity, windSpeed, precipitation }) {
  const { tempUnit, windUnit } = usePreferences();

  const displayTemp = tempUnit === 'F' ? (temp * 9/5) + 32 : temp;

  // <--- NEW: Wind speed conversion logic
  const displayWindSpeed = windUnit === 'kmh' ? (windSpeed * 3.6) : windSpeed; // Convert m/s to km/h

  return (
    <div className="weather-card">
      <h2 className="card-title">Current Weather</h2>
      <div className="card-content">
        <p className="weather-info">
          Temperature: {displayTemp.toFixed(1)}°{tempUnit}
        </p>
        <p className="weather-info">Humidity: {humidity}%</p>

        {/* <--- NEW: Display Wind Speed and Precipitation conditionally */}
        {windSpeed !== undefined && windSpeed !== null && (
            <p className="weather-info">
                Wind Speed: {displayWindSpeed.toFixed(1)} {windUnit === 'kmh' ? 'km/h' : 'm/s'}
            </p>
        )}
        {precipitation !== undefined && precipitation !== null && (
            <p className="weather-info">Precipitation: {precipitation.toFixed(1)} mm</p>
        )}
      </div>
    </div>
  );
}