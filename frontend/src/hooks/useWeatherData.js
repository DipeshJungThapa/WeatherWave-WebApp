// frontend/src/hooks/useWeatherData.js

import { useState, useEffect } from 'react';
import axios from 'axios';

const useWeatherData = (location) => {
    const [weatherData, setWeatherData] = useState(null);
    const [aqiData, setAqiData] = useState(null);
    const [forecastData, setForecastData] = useState(null);
    const [predictionData, setPredictionData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [geoError, setGeoError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            setError(null);
            setGeoError(null);

            let fetchLocation = location;
            let queryType = 'city';
            let cityName = null;

            // If location is not provided, try to get current geo-location
            if (!location) {
                if (navigator.geolocation) {
                    try {
                        const position = await new Promise((resolve, reject) => {
                            navigator.geolocation.getCurrentPosition(resolve, reject, {
                                enableHighAccuracy: true,
                                timeout: 10000,
                                maximumAge: 0
                            });
                        });
                        fetchLocation = { lat: position.coords.latitude, lon: position.coords.longitude };
                        queryType = 'coords';
                    } catch (geoErr) {
                        setGeoError("Geolocation denied or unavailable. Please select a city or enable location.");
                        setLoading(false);
                        return;
                    }
                } else {
                    setGeoError("Geolocation is not supported by your browser. Please select a city.");
                    setLoading(false);
                    return;
                }
            } else if (typeof location === 'object' && location.lat && location.lon) {
                queryType = 'coords';
                fetchLocation = location;
            } else {
                cityName = fetchLocation; // If location is a string, it's a city name
            }

            const isCoords = queryType === 'coords';
            const queryParam = isCoords
                ? `lat=${fetchLocation.lat}&lon=${fetchLocation.lon}`
                : `city=${fetchLocation}`;

            try {
                // Fetch weather data
                const weatherResponse = await axios.get(`http://localhost:8000/api/current-weather/?${queryParam}`);
                setWeatherData(weatherResponse.data);

                // Extract city name from weather data if fetched by coordinates
                if (isCoords && weatherResponse.data && weatherResponse.data.name) {
                    cityName = weatherResponse.data.name;
                }

                // Fetch forecast data
                const forecastResponse = await axios.get(`http://localhost:8000/api/forecast/?${queryParam}`);
                setForecastData(forecastResponse.data.forecast);

                // Try to fetch AQI data, but don't fail if it's not available
                try {
                    const aqiResponse = await axios.get(`http://localhost:8000/api/aqi/?${queryParam}`);
                    setAqiData(aqiResponse.data);
                } catch (aqiError) {
                    console.warn("AQI data not available:", aqiError.response?.data?.error || aqiError.message);
                    setAqiData(null); // Set to null if AQI fails
                }

                // Fetch prediction data using the city name
                if (cityName) {
                    try {
                         const predictionResponse = await axios.post(`http://localhost:8000/api/predict-city/`, { city: cityName });
                         console.log("Prediction Response Status:", predictionResponse.status); // Log status
                         console.log("Prediction Response Data:", predictionResponse.data); // Log prediction data
                         setPredictionData(predictionResponse.data);
                    } catch (predictionError) {
                         console.warn("Prediction data fetch failed:", predictionError.response?.status, predictionError.response?.data || predictionError.message);
                         setPredictionData(null); // Set to null if prediction fails
                    }
                }

            } catch (err) {
                console.error("Error fetching weather data:", err);
                if (err.response) {
                    // The request was made and the server responded with a status code
                    // that falls out of the range of 2xx
                    setError(`Server Error: ${err.response.status} - ${err.response.data?.detail || err.response.data?.message || 'Something went wrong.'}`);
                } else if (err.request) {
                    // The request was made but no response was received
                    setError("Network Error: No response from server. Check if backend is running.");
                } else {
                    // Something else happened while setting up the request
                    setError("An unexpected error occurred while fetching data.");
                }
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [location]);

    return { weatherData, aqiData, forecastData, predictionData, loading, error, geoError };
};

export default useWeatherData;