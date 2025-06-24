// src/components/PredictionCard.jsx
import React from 'react';
import './PredictionCard.css'; // Make sure this CSS file exists
import { usePreferences } from '../context/PreferencesContext'; // Import usePreferences

export default function PredictionCard({ prediction }) {
  const { tempUnit } = usePreferences();

  // Ensure prediction is an object and has mlTemp and fiveDayForecast
  const mlPredictedTemp = prediction?.mlTemp ?? 'N/A';
  const fiveDayForecast = prediction?.fiveDayForecast || [];

  // Convert ML predicted temp if unit is Fahrenheit
  const displayMlTemp = mlPredictedTemp !== 'N/A'
    ? (tempUnit === 'F' ? (mlPredictedTemp * 9/5) + 32 : mlPredictedTemp).toFixed(1)
    : 'N/A';

  // Helper function to format date (example: Mon, Jun 20)
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
    } catch {
      return dateString; // Return as is if parsing fails
    }
  };

  return (
    <div className="prediction-card">
      <h2 className="card-title">Tomorrow's Forecast & ML Prediction</h2> {/* Updated Title */}
      <div className="card-content">
        {/* --- ML Predicted Temperature Section --- */}
        <div className="ml-prediction-section">
          <h3 className="section-title">ML Predicted Temperature (Tomorrow)</h3>
          <p className="prediction-info">
            Temperature: {displayMlTemp}°{tempUnit}
          </p>
          <p className="prediction-note">
            (This prediction comes from your trained ML model for tomorrow's 2m temperature.)
          </p>
        </div>

        {/* --- 5-Day API Forecast Section --- */}
        <div className="five-day-forecast-section">
          <h3 className="section-title">5-Day Forecast (API)</h3>
          {fiveDayForecast.length > 0 ? (
            <div className="forecast-list">
              {fiveDayForecast.map((day, index) => (
                <div key={index} className="forecast-item">
                  <p className="forecast-date">{formatDate(day.date)}</p> {/* Assuming 'date' property */}
                  <p className="forecast-temp">
                    Temp: {tempUnit === 'F' ? ((day.temp || 0) * 9/5 + 32).toFixed(1) : (day.temp || 0).toFixed(1)}°{tempUnit}
                  </p>
                  {/* Add other details like min/max, weather condition icon etc., when available */}
                  <p className="forecast-desc">{day.condition || 'N/A'}</p> {/* Assuming 'condition' property */}
                </div>
              ))}
            </div>
          ) : (
            <p className="no-forecast-message">
              No 5-day forecast data available. (Will be provided by API)
            </p>
          )}
        </div>
      </div>
    </div>
  );
}