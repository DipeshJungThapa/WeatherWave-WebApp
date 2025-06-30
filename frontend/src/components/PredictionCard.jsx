// frontend/src/components/PredictionCard.jsx
import React from 'react';
import './PredictionCard.css';

// Receive both prediction and forecast props
function PredictionCard({ prediction, forecast }) {
  return (
    <div className="prediction-card card">
      <h3>Tomorrow's Forecast & ML Prediction</h3>
      <p>ML Predicted Temperature (Tomorrow):</p>
      <p className="prediction-temp">
        {prediction !== null && prediction !== undefined
          ? `${prediction.toFixed(1)}°C` // Format to one decimal place
          : 'N/A'}
      </p>
      <p className="prediction-info">
        (This prediction comes from your trained ML model for tomorrow's 2m temperature.)
      </p>

      {/* NEW: Display 5-Day Forecast */}
      <p>5-Day Forecast:</p>
      <div className="forecast-list">
        {forecast && forecast.length > 0 ? (
          forecast.map((day, index) => (
            <div key={index} className="forecast-item">
              <p className="forecast-date">{day.date}:</p>
              <p>Avg: {day.Weather.avg_temp.toFixed(1)}°C</p>
              <p>Max: {day.Weather.max_temp.toFixed(1)}°C</p>
              <p>Min: {day.Weather.min_temp.toFixed(1)}°C</p>
              {/* You can add icon/description if your API provides it later */}
            </div>
          ))
        ) : (
          <p>No 5-day forecast data available. (Will be provided by API)</p>
        )}
      </div>
    </div>
  );
}

export default PredictionCard;