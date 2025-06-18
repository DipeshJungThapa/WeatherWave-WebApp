// src/components/PredictionCard.jsx
import React from 'react';
import './PredictionCard.css'; // Import the new CSS file

export default function PredictionCard({ prediction }) {
  return (
    <div className="prediction-card">
      <h3 className="prediction-card-title">Tomorrow's Forecast</h3>
      <div className="prediction-card-item">Next: {prediction ?? '–'}°C</div>
    </div>
  );
}