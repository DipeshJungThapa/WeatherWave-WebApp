// src/components/PredictionCard.jsx
import React from 'react';
import "./PredictionCard.css";
const PredictionCard = ({ prediction, forecast, loading, error }) => {
    if (loading) {
        return <div className="prediction-card">Loading predictions and forecast...</div>;
    }

    const displayPrediction = prediction !== null && prediction !== undefined && !isNaN(prediction) 
                            ? `${prediction.toFixed(1)}°C` 
                            : 'N/A';

    const hasForecast = forecast && Array.isArray(forecast) && forecast.length > 0;

    return (
        <div className="prediction-card">
            <h2 className="card-title">Temperature Predictions</h2>
            <div className="card-content">
                <div className="ml-prediction-section">
                    <p className="section-title">ML Predicted Temperature</p>
                    <p className="prediction-info">{displayPrediction}</p>
                    <p className="prediction-note">
                        {prediction !== null ? "Prediction for the next 24 hours based on current data." : "Prediction data not available."}
                    </p>
                </div>

                <div className="five-day-forecast-section">
                    <p className="section-title">5-Day Forecast (Avg Temp)</p>
                    {hasForecast ? (
                        <div className="forecast-list">
                            {forecast.map((day, index) => (
                                <div key={index} className="forecast-item">
                                    <p className="forecast-date">{day.date}</p>
                                    <p className="forecast-temp">
                                        {day.Weather?.avg_temp !== undefined && !isNaN(day.Weather?.avg_temp)
                                            ? `${day.Weather.avg_temp.toFixed(1)}°C`
                                            : 'N/A'}
                                    </p>
                                    {/* You can add more forecast details here if available from API */}
                                    {/* <p className="forecast-desc">{day.Weather?.description || ''}</p> */}
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p className="no-forecast-message">No 5-day forecast data available.</p>
                    )}
                </div>
            </div>
            {error && (
                <p style={{ color: 'orange', fontSize: '0.8em', marginTop: '10px' }}>
                    Error fetching prediction/forecast: {error.message || 'Check connection or API key.'}
                </p>
            )}
        </div>
    );
};

export default PredictionCard;