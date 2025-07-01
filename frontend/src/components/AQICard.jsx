// src/components/AQICard.jsx
import React from 'react';
import './AQICard.css';
const getAqiCategory = (aqi) => {
    if (aqi === null || aqi === undefined || isNaN(aqi)) return { text: 'N/A', color: '#999' };
    if (aqi <= 50) return { text: 'Good', color: '#4CAF50' };
    if (aqi <= 100) return { text: 'Moderate', color: '#FFEB3B' };
    if (aqi <= 150) return { text: 'Unhealthy for Sensitive Groups', color: '#FF9800' };
    if (aqi <= 200) return { text: 'Unhealthy', color: '#F44336' };
    if (aqi <= 300) return { text: 'Very Unhealthy', color: '#9C27B0' };
    return { text: 'Hazardous', color: '#6A1B9A' };
};

const getAqiRecommendation = (category) => {
    switch (category) {
        case 'Good': return "Air quality is satisfactory, and air pollution poses little or no risk.";
        case 'Moderate': return "Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution.";
        case 'Unhealthy for Sensitive Groups': return "Members of sensitive groups may experience health effects. The general public is less likely to be affected.";
        case 'Unhealthy': return "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.";
        case 'Very Unhealthy': return "Health warnings of emergency conditions. The entire population is more likely to be affected.";
        case 'Hazardous': return "Health alert: everyone may experience more serious health effects.";
        case 'N/A': return "AQI data not available. No specific recommendation at this time.";
        default: return "No specific recommendation.";
    }
};

const AQICard = ({ aqi, loading, error }) => {
    if (loading) {
        return <div className="aqi-card">Loading AQI...</div>;
    }

    const displayAqi = aqi !== null && aqi !== undefined && !isNaN(aqi) ? Math.round(aqi) : 'N/A';
    const aqiCategory = getAqiCategory(displayAqi);
    const recommendation = getAqiRecommendation(aqiCategory.text);

    return (
        <div className="aqi-card">
            <h2 className="card-title">Air Quality Index</h2>
            <div className="card-content">
                <div className="aqi-overall">
                    <p className="aqi-label">Overall AQI</p>
                    <p className="aqi-value" style={{ color: aqiCategory.color }}>
                        {displayAqi}
                    </p>
                    <p className="aqi-label">Category: {aqiCategory.text}</p>
                </div>

                <div className="aqi-recommendation">
                    <h3 className="recommendation-title">Health Recommendation:</h3>
                    <p className="recommendation-text">{recommendation}</p>
                </div>

                {error && (
                    <p style={{ color: 'orange', fontSize: '0.8em', marginTop: '10px' }}>
                        Error fetching detailed AQI: {error.message || 'Check connection or API key.'}
                    </p>
                )}
            </div>
        </div>
    );
};

export default AQICard;