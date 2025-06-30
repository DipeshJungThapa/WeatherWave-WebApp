// frontend/src/pages/Dashboard.jsx
import React, { useEffect } from 'react';
import './Dashboard.css';
import DistrictSelector from '../components/DistrictSelector';
import WeatherCard from '../components/WeatherCard';
import AQICard from '../components/AQICard';
import PredictionCard from '../components/PredictionCard';
import useWeatherData from '../hooks/useWeatherData';
import useGeolocation from '../hooks/useGeolocation';
import { useDistrict } from '../context/DistrictContext';
import { useAuth } from '../context/AuthContext';
import useFavourites from '../hooks/useFavourites';
import { usePreferences } from '../context/PreferencesContext';
import { useOnlineStatus } from "../hooks/useOnlineStatus";

export default function Dashboard() {
  const { location, permissionDenied } = useGeolocation();
  const latitude = location ? location.lat : null;
  const longitude = location ? location.lon : null;

  const { district, setDistrict } = useDistrict();
  const { token } = useAuth();
  const { addFavorite, favorites, loading: favLoading, error: favError, removeFavorite } = useFavourites();

  const { tempUnit, setTempUnit, windUnit, setWindUnit, theme, setTheme } = usePreferences();

  // NEW: Destructure forecast from useWeatherData
  const { weather, aqi, prediction, forecast, loading: weatherLoading, error: weatherError } = useWeatherData(latitude, longitude, district);

  const isOnline = useOnlineStatus();

  useEffect(() => {
    if (latitude && longitude) {
      console.log("Dashboard: Data will be fetched using Geolocation coordinates:", { latitude, longitude });
    } else if (permissionDenied) {
      console.log("Dashboard: Geolocation permission denied. Data will be fetched using selected district:", district);
    } else {
      console.log("Dashboard: Geolocation not available or pending. Data will be fetched using selected district:", district);
    }
  }, [latitude, longitude, permissionDenied, district]);

  const handleAddFavorite = async () => {
    if (!token) {
      alert("Please log in to add favorites.");
      return;
    }
    if (!district) {
      alert("Please select a district to add to favorites.");
      return;
    }
    await addFavorite(district);
    alert(`District '${district}' added to favorites! (or attempted to add)`);
  };

  const handleRemoveFavorite = async (favDistrict) => {
    if (!token) {
      alert("Please log in to remove favorites.");
      return;
    }
    await removeFavorite(favDistrict);
    alert(`District '${favDistrict}' removed from favorites! (or attempted to remove)`);
  };

  const toggleTempUnit = () => {
    setTempUnit(prevUnit => prevUnit === 'C' ? 'F' : 'C');
  };

  const toggleWindUnit = () => {
    setWindUnit(prevUnit => prevUnit === 'ms' ? 'kmh' : 'ms');
  };

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'dark' ? 'light' : 'dark');
  };

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">WeatherWave Dashboard</h1>

      {!isOnline && (
        <div className="offline-banner">
          🔌 You are offline. Weather data cannot be fetched.
        </div>
      )}

      <DistrictSelector />

      {token && (
        <button
          onClick={handleAddFavorite}
          className="add-favorite-button"
        >
          ⭐ Add {district || 'current'} to Favorites
        </button>
      )}

      <div className="preferences-panel">
        <div className="preference-group">
          <label>Temperature Unit:</label>
          <button
            onClick={toggleTempUnit}
            className={tempUnit === 'C' ? 'active-unit-button' : 'unit-button'}
          >
            °C
          </button>
          <button
            onClick={toggleTempUnit}
            className={tempUnit === 'F' ? 'active-unit-button' : 'unit-button'}
          >
            °F
          </button>
        </div>

        <div className="preference-group">
          <label>Wind Speed Unit:</label>
          <button
            onClick={toggleWindUnit}
            className={windUnit === 'ms' ? 'active-unit-button' : 'unit-button'}
          >
            m/s
          </button>
          <button
            onClick={toggleWindUnit}
            className={windUnit === 'kmh' ? 'active-unit-button' : 'unit-button'}
          >
            km/h
          </button>
        </div>

        <div className="preference-group">
          <label>Theme:</label>
          <button
            onClick={toggleTheme}
            className={theme === 'dark' ? 'active-unit-button' : 'unit-button'}
          >
            Dark
          </button>
          <button
            onClick={toggleTheme}
            className={theme === 'light' ? 'active-unit-button' : 'unit-button'}
          >
            Light
          </button>
        </div>
      </div>

      {(weatherLoading || favLoading) && <p className="loading-message">Loading data...</p>}
      {(weatherError || favError) && <p className="error-message">Error: {weatherError || favError}</p>}

      <div className="dashboard-cards-container">
        {!weatherLoading && weather && (
          <>
            <WeatherCard
              temp={weather.temp}
              humidity={weather.humidity}
              windSpeed={weather.windSpeed}
              precipitation={weather.precipitation}
            />
            <AQICard aqi={aqi} />
            {/* NEW: Pass forecast to PredictionCard */}
            <PredictionCard prediction={prediction} forecast={forecast} />
          </>
        )}

        {!weatherLoading && !weatherError && !weather && (
          <p className="initial-message">Select a district to fetch data.</p>
        )}
      </div>

      {token && favorites && favorites.length > 0 && (
        <div className="favorite-districts-section">
          <h3>Your Favorite Districts:</h3>
          <div className="favorite-buttons-container">
            {favorites.map((fav, index) => (
              <button
                key={fav.id || index}
                onClick={() => setDistrict(fav.name || fav)}
                className="favorite-item-button"
              >
                {fav.name || fav}
                <span
                  onClick={(e) => { e.stopPropagation(); handleRemoveFavorite(fav.name || fav); }}
                  className="remove-favorite-button"
                >❌</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}