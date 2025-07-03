// frontend/src/hooks/useWeatherData.js (or .jsx)

import { useState, useEffect } from 'react';
import axios from 'axios';

const useWeatherData = (location) => {
    const [weatherData, setWeatherData] = useState(null);
    const [aqiData, setAqiData] = useState(null);
    const [forecastData, setForecastData] = useState(null);
    const [predictionData, setPredictionData] = useState(null); // Assuming you have a prediction endpoint
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [geoError, setGeoError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            setError(null);
            setGeoError(null);

            let fetchLocation = location;
            let queryType = 'city'; // Default to city

            // If location is not provided (e.g., initial load), try to get current geo-location
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
                        return; // Stop execution if geolocation fails
                    }
                } else {
                    setGeoError("Geolocation is not supported by your browser. Please select a city.");
                    setLoading(false);
                    return; // Stop execution if geolocation not supported
                }
            } else if (typeof location === 'object' && location.lat && location.lon) {
                queryType = 'coords';
                fetchLocation = location;
            }

            const isCoords = queryType === 'coords';
            const queryParam = isCoords
                ? `lat=${fetchLocation.lat}&lon=${fetchLocation.lon}`
                : `city=${fetchLocation}`;

            try {
                // --- UPDATE THESE URLs TO INCLUDE /api/ ---
                const weatherResponse = await axios.get(`http://localhost:8000/api/current-weather/?${queryParam}`);
                setWeatherData(weatherResponse.data);

                const aqiResponse = await axios.get(`http://localhost:8000/api/aqi/?${queryParam}`);
                setAqiData(aqiResponse.data);

                const forecastResponse = await axios.get(`http://localhost:8000/api/forecast/?${queryParam}`);
                setForecastData(forecastResponse.data.forecast); // Assuming forecast data is nested under 'forecast' key

                // If you have prediction APIs, uncomment and use them
                // const predictionCityResponse = await axios.get(`http://localhost:8000/api/predict-city/?city=${fetchLocation}`);
                // const predictionGeoResponse = await axios.get(`http://localhost:8000/api/predict-geo/?lat=${fetchLocation.lat}&lon=${fetchLocation.lon}`);
                // setPredictionData(predictionCityResponse.data || predictionGeoResponse.data); // Adjust as per your prediction data structure

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
    }, [location]); // Re-run effect when location prop changes

    return { weatherData, aqiData, forecastData, predictionData, loading, error, geoError };
};

export default useWeatherData;