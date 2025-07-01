import React, { useEffect } from 'react';
import './Dashboard.css';
import DistrictSelector from '../components/DistrictSelector';
import WeatherCard from '../components/WeatherCard';
import AQICard from '../components/AQICard';
import PredictionCard from '../components/PredictionCard';
import { useWeatherData } from '../hooks/useWeatherData.jsx'; // Correct import path and named export
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

  const { district, setDistrict } = useDistrict(); // This is `selectedDistrict` in useWeatherData
  const { token } = useAuth();
  const { addFavorite, favorites, loading: favLoading, error: favError, removeFavorite } = useFavourites();

  const { tempUnit, setTempUnit, windUnit, setWindUnit, theme, setTheme } = usePreferences();

  // Updated: Use new state names from useWeatherData hook
  const {
    weatherData,
    aqiData,
    predictionData,
    forecastData,
    overallLoading, // This combines loading states from all fetches
    overallError,   // This combines error states from all fetches
  } = useWeatherData(latitude, longitude, district); // Pass latitude, longitude, and district

  const isOnline = useOnlineStatus();

  // No longer need this useEffect for console logs as it's handled in useWeatherData
  // useEffect(() => {
  //   if (latitude && longitude) {
  //     console.log("Dashboard: Data will be fetched using Geolocation coordinates:", { latitude, longitude });
  //   } else if (permissionDenied) {
  //     console.log("Dashboard: Geolocation permission denied. Data will be fetched using selected district:", district);
  //   } else {
  //     console.log("Dashboard: Geolocation not available or pending. Data will be fetched using selected district:", district);
  //   }
  // }, [latitude, longitude, permissionDenied, district]);

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
  };

  const handleRemoveFavorite = async (favDistrict) => {
    if (!token) {
      alert("Please log in to remove favorites.");
      return;
    }
    await removeFavorite(favDistrict);
  };

  const handleRemoveClick = (e, districtName) => {
    e.stopPropagation();
    handleRemoveFavorite(districtName);
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

      {overallLoading && <p className="loading-message">Loading data...</p>}
      {overallError && <p className="error-message">Error: {overallError.message || overallError}</p>}

      <div className="dashboard-cards-container">
        {/* Only render weather cards if not loading and weather data exists and no overall error */}
        {!overallLoading && !overallError && weatherData && (
          <>
            <WeatherCard
              temp={weatherData.temp !== undefined && weatherData.temp !== null ? weatherData.temp : 'N/A'}
              humidity={weatherData.humidity !== undefined && weatherData.humidity !== null ? weatherData.humidity : 'N/A'}
              windSpeed={weatherData.wind_speed !== undefined && weatherData.wind_speed !== null ? weatherData.wind_speed : 'N/A'}
              precipitation={weatherData.precip !== undefined && weatherData.precip !== null ? weatherData.precip : 'N/A'}
              description={weatherData.description !== undefined && weatherData.description !== null ? weatherData.description : 'N/A'}
            />
            {/* Render AQICard only if aqiData is available */}
            {aqiData !== null && aqiData !== undefined && <AQICard aqi={aqiData} />}
            {/* Render PredictionCard only if predictionData is available */}
            {predictionData !== null && predictionData !== undefined && <PredictionCard prediction={predictionData} forecast={forecastData} />}
          </>
        )}

        {/* Display initial message if no data is loading, no error, and no weather data */}
        {!overallLoading && !overallError && !weatherData && (
          <p className="initial-message">Select a district or enable geolocation to fetch data.</p>
        )}
      </div>

      {token && favorites && favorites.length > 0 && (
        <div className="favorite-districts-section">
          <h3>Your Favorite Districts:</h3>
          <div className="favorite-buttons-container">
            {favorites.map((fav, index) => (
              <button
                key={fav.id || index}
                onClick={() => setDistrict(fav.district_name)}
                className="favorite-item-button"
              >
                {fav.district_name}
                <span
                  onClick={(e) => handleRemoveClick(e, fav.district_name)}
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