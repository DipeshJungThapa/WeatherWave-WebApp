// frontend/src/hooks/useWeatherData.jsx
import { useState, useEffect, useCallback } from 'react';
import axiosInstance from '../api/axiosInstance'; // Correct import path for the new axiosInstance
import { useAuth } from '../context/AuthContext';
import { useDistrict } from '../context/DistrictContext'; // Assuming this provides selectedDistrict

export const useWeatherData = (latitude, longitude, cityFromPreferences = null) => {
    const { selectedDistrict } = useDistrict(); // Get selected district from context
    const { token } = useAuth(); // Get the authentication token from context

    const [weatherData, setWeatherData] = useState(null);
    const [aqiData, setAqiData] = useState(null);
    const [predictionData, setPredictionData] = useState(null);
    const [forecastData, setForecastData] = useState(null);
    const [overallLoading, setOverallLoading] = useState(true);
    const [overallError, setOverallError] = useState(null);

    // fetchData is now independent of getAuthHeaders, as interceptor handles auth
    const fetchData = useCallback(async () => {
        console.log('useWeatherData: fetchData called. Token:', token ? 'Present' : 'Missing');

        if (!token) {
            console.log('useWeatherData: No token available. Skipping API calls.');
            setOverallLoading(false);
            setOverallError(new Error('Authentication token not available. Please log in.'));
            setWeatherData(null);
            setAqiData(null);
            setPredictionData(null);
            setForecastData(null);
            return;
        }

        setOverallLoading(true);
        setOverallError(null);

        // Determine the city/location to use for requests
        const effectiveCity = selectedDistrict || cityFromPreferences;
        console.log('useWeatherData: Effective city for requests:', effectiveCity);

        const requests = [];
        let weatherRequestPromise;

        // --- Weather Data Fetch (Conditional based on geolocation or selected city) ---
        if (latitude && longitude) {
            console.log("Fetching weather using lat/lon...");
            // Use relative path because axiosInstance has baseURL
            weatherRequestPromise = axiosInstance.get('/weather/', { params: { lat: latitude, lon: longitude } })
                .then(response => {
                    console.log('useWeatherData: Weather by geo response:', response.data);
                    // Backend's get_current_weather returns: city, temp, humidity, description, wind_speed
                    setWeatherData({
                        city: response.data.city,
                        temp: response.data.temp, // Assuming backend sends 'temp'
                        humidity: response.data.humidity,
                        wind_speed: response.data.wind_speed,
                        description: response.data.description,
                        precip: response.data.precip || 0, // Add precip if available
                    });
                })
                .catch(err => {
                    console.error('useWeatherData: Error fetching weather by geo:', err.response?.data || err.message);
                    setOverallError(prev => prev || err); // Set error only if not already set
                    setWeatherData(null);
                });
        } else if (effectiveCity) {
            console.log("Fetching weather using city name...");
            // Use relative path
            weatherRequestPromise = axiosInstance.post('/default_weather/', { city: effectiveCity })
                .then(response => {
                    console.log('useWeatherData: Weather by city response:', response.data);
                    // Backend's get_current_weather_default returns: city, temperature, description, humidity, wind_speed
                    setWeatherData({
                        city: response.data.city,
                        temp: response.data.temperature, // Assuming backend sends 'temperature'
                        humidity: response.data.humidity,
                        wind_speed: response.data.wind_speed,
                        description: response.data.description,
                        precip: response.data.precipitation || 0, // Add precip if available
                    });
                })
                .catch(err => {
                    console.error('useWeatherData: Error fetching weather by city:', err.response?.data || err.message);
                    setOverallError(prev => prev || err);
                    setWeatherData(null);
                });
        } else {
            // No valid source for weather data
            setOverallLoading(false);
            setWeatherData(null);
            setAqiData(null);
            setPredictionData(null);
            setForecastData(null);
            return; // Exit if no valid parameters to fetch
        }
        requests.push(weatherRequestPromise);


        // --- AQI Request ---
        requests.push(axiosInstance.get('/aqi/') // Use relative path
            .then(response => {
                console.log('useWeatherData: AQI response:', response.data);
                setAqiData(response.data.AQI_Value); // Assuming backend returns { "AQI_Value": ... }
            })
            .catch(err => {
                console.error('useWeatherData: Error fetching AQI:', err.response?.data || err.message);
                setOverallError(prev => prev || err);
                setAqiData(null);
            }));

        // --- Prediction Request (predict_city if effectiveCity, else predict_geo) ---
        if (effectiveCity) {
            requests.push(axiosInstance.post('/predict_city/', { city: effectiveCity }) // Use relative path
                .then(response => {
                    console.log('useWeatherData: Prediction by city response:', response.data);
                    setPredictionData(response.data.predicted_temp); // Assuming backend returns { "predicted_temp": ... }
                })
                .catch(err => {
                    console.error('useWeatherData: Error fetching prediction by city:', err.response?.data || err.message);
                    setOverallError(prev => prev || err);
                    setPredictionData(null);
                }));
        } else {
            requests.push(axiosInstance.post('/predict_geo/', {}) // Use relative path, empty body for POST
                .then(response => {
                    console.log('useWeatherData: Prediction by geo response:', response.data);
                    setPredictionData(response.data.predicted_temp); // Assuming backend returns { "predicted_temp": ... }
                })
                .catch(err => {
                    console.error('useWeatherData: Error fetching prediction by geo:', err.response?.data || err.message);
                    setOverallError(prev => prev || err);
                    setPredictionData(null);
                }));
        }

        // --- Forecast Request ---
        requests.push(axiosInstance.get('/forecast/') // Use relative path
            .then(response => {
                console.log('useWeatherData: Forecast response:', response.data);
                setForecastData(response.data.forecast); // Assuming backend returns { "forecast": [...] }
            })
            .catch(err => {
                console.error('useWeatherData: Error fetching forecast:', err.response?.data || err.message);
                setOverallError(prev => prev || err);
                setForecastData(null);
            }));

        try {
            await Promise.all(requests);
        } catch (error) {
            // Individual errors are already set by their .catch blocks
            console.error('useWeatherData: One or more data fetches failed:', error);
        } finally {
            setOverallLoading(false);
            console.log('useWeatherData: Data fetch completed.');
        }
    }, [token, selectedDistrict, latitude, longitude, cityFromPreferences]); // Removed getAuthHeaders from deps

    useEffect(() => {
        // Trigger fetch if token is available and either geolocation or a district is selected
        if (token && ((latitude !== null && longitude !== null) || selectedDistrict || cityFromPreferences)) {
            fetchData();
        } else if (!token) {
            // If no token, clear all data and set error
            setOverallLoading(false);
            setOverallError(new Error('Authentication token not available. Please log in.'));
            setWeatherData(null);
            setAqiData(null);
            setPredictionData(null);
            setForecastData(null);
        } else {
            // No token, no district, no location - just set loading to false and no data
            setOverallLoading(false);
            setWeatherData(null);
            setAqiData(null);
            setPredictionData(null);
            setForecastData(null);
            setOverallError(null);
        }
    }, [fetchData, token, latitude, longitude, selectedDistrict, cityFromPreferences]); // Added all dependencies to fetchData's effect

    return { weatherData, aqiData, predictionData, forecastData, overallLoading, overallError, fetchData };
};

export default useWeatherData;