// src/components/WeatherCard.jsx
import React from 'react';
import './WeatherCard.css';
const WeatherCard = ({ weather, loading, error }) => {
    if (loading) {
        return <div className="weather-card">Loading weather...</div>;
    }

    if (error) {
        return <div className="weather-card error">Error: {error.message || 'Failed to load weather data'}</div>;
    }

    // Use optional chaining for safer access
    const displayCity = weather?.city || 'N/A';
    const displayTemp = weather?.temp !== undefined ? `${weather.temp}°C` : 'N/A';
    const displayDescription = weather?.description || 'N/A';
    const displayHumidity = weather?.humidity !== undefined ? `${weather.humidity}%` : 'N/A';
    const displayWindSpeed = weather?.wind_speed !== undefined ? `${weather.wind_speed} m/s` : 'N/A';

    return (
        <div className="weather-card">
            <h2 className="weather-card-title">Current Weather for {displayCity}</h2>
            <p className="weather-card-item">Temperature: {displayTemp}</p>
            <p className="weather-card-item">Description: {displayDescription}</p>
            <p className="weather-card-item">Humidity: {displayHumidity}</p>
            <p className="weather-card-item">Wind Speed: {displayWindSpeed}</p>
        </div>
    );
};

export default WeatherCard;