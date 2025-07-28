// frontend/src/hooks/useWeatherData.js

import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const CACHE_DURATION = 1140 * 5 * 60 * 1000; // Cache data for 5 minutes

const useWeatherData = (location) => {
    const [weatherData, setWeatherData] = useState(null);
    const [aqiData, setAqiData] = useState(null);
    const [forecastData, setForecastData] = useState(null);
    const [predictionData, setPredictionData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [geoError, setGeoError] = useState(null);
    const [isOffline, setIsOffline] = useState(false);

    const getLocationKey = useCallback((loc) => {
        if (typeof loc === 'string') return loc;
        if (typeof loc === 'object' && loc.lat && loc.lon) return `${loc.lat},${loc.lon}`;
        return 'default';
    }, []); // Memoize getLocationKey

    useEffect(() => {
        const locationKey = getLocationKey(location);
        let cachedData = localStorage.getItem(`weatherCache_${locationKey}`);
        let parsedCache = null;
        let usedInitialCache = false;

        if (cachedData) {
            try {
                parsedCache = JSON.parse(cachedData);
                const cacheTimestamp = parsedCache.timestamp;
                const now = new Date().getTime();

                if (now - cacheTimestamp < CACHE_DURATION) {
                    // Use cached data immediately if not expired
                    setWeatherData(parsedCache.weatherData);
                    setAqiData(parsedCache.aqiData);
                    setForecastData(parsedCache.forecastData);
                    setPredictionData(parsedCache.predictionData);
                    setIsOffline(true); // Temporarily assume offline if using cache initially
                    setLoading(false);
                    usedInitialCache = true;
                    console.log("Using valid cached data for", locationKey);
                     // We still proceed to fetch online to update the cache
                } else {
                    // Cache expired
                    console.log("Cache expired for", locationKey);
                    localStorage.removeItem(`weatherCache_${locationKey}`);
                }
            } catch (e) {
                console.error("Error parsing cache:", e);
                localStorage.removeItem(`weatherCache_${locationKey}`);
            }
        }

        const controller = new AbortController(); // To cancel fetch on unmount or location change
        const signal = controller.signal;

        const fetchData = async () => {

            // If initial cache was used, set loading to false but still fetch in background
            if (!usedInitialCache) {
                 setLoading(true);
                 // Clear previous data when starting a new fetch, unless initial cache was used
                 setWeatherData(null);
                 setAqiData(null);
                 setForecastData(null);
                 setPredictionData(null);
            }

            setError(null);
            setGeoError(null);
            setIsOffline(false); // Assume online at the start of a fetch attempt

            let fetchLocation = location;
            let queryType = 'city';
            let currentCityName = null;

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
                         // Update locationKey after getting geo-location for caching
                         // Need to get locationKey again here as fetchLocation might have changed
                        locationKey = getLocationKey(fetchLocation);
                    } catch (geoErr) {
                        console.error("Geolocation error:", geoErr);
                        setGeoError("Geolocation denied or unavailable. Please select a city or enable location.");
                         // If geo-location fails, we cannot fetch, so check cache as a last resort
                         attemptLoadFromCache(locationKey, "Geolocation error. Showing cached data if available.");
                        setLoading(false);
                        return;
                    }
                } else {
                    setGeoError("Geolocation is not supported by your browser. Please select a city.");
                     attemptLoadFromCache(locationKey, "Geolocation not supported. Showing cached data if available.");
                    setLoading(false);
                    return;
                }
            } else if (typeof location === 'object' && location.lat && location.lon) {
                queryType = 'coords';
                fetchLocation = location;
                 // locationKey is already set from the start of useEffect
            } else {
                currentCityName = fetchLocation; // If location is a string, it's a city name
                 // locationKey is already set from the start of useEffect
            }


            const isCoords = queryType === 'coords';
            const queryParam = isCoords
                ? `lat=${fetchLocation.lat}&lon=${fetchLocation.lon}`
                : `city=${fetchLocation}`;

            try {
                // Fetch weather data
                const weatherResponse = await axios.get(`http://localhost:8000/api/current-weather/?${queryParam}`, { signal });
                setWeatherData(weatherResponse.data);

                // Extract city name from weather data if fetched by coordinates
                if (isCoords && weatherResponse.data && weatherResponse.data.name) {
                    currentCityName = weatherResponse.data.name;
                }

                // Fetch forecast data
                const forecastResponse = await axios.get(`http://localhost:8000/api/forecast/?${queryParam}`, { signal });
                setForecastData(forecastResponse.data.forecast);

                // Try to fetch AQI data, but don't fail if it's not available
                let currentAqiData = null;
                try {
                    const aqiResponse = await axios.get(`http://localhost:8000/api/aqi/?${queryParam}`, { signal });
                    setAqiData(aqiResponse.data);
                    currentAqiData = aqiResponse.data;
                } catch (aqiError) {
                    if (axios.isCancel(aqiError)) return; // Ignore if request was cancelled
                    console.warn("AQI data not available:", aqiError.response?.data?.error || aqiError.message);
                    setAqiData(null); // Set to null if AQI fails
                }

                // Fetch prediction data using the city name
                let currentPredictionData = null;
                if (currentCityName) {
                    try {
                         const predictionResponse = await axios.post(`http://localhost:8000/api/predict-city/`, { city: currentCityName }, { signal });
                         console.log("Prediction Response Status:", predictionResponse.status); // Log status
                         console.log("Prediction Response Data:", predictionResponse.data); // Log prediction data
                         setPredictionData(predictionResponse.data);
                         currentPredictionData = predictionResponse.data;
                    } catch (predictionError) {
                         if (axios.isCancel(predictionError)) return; // Ignore if request was cancelled
                         console.warn("Prediction data fetch failed:", predictionError.response?.status, predictionError.response?.data || predictionError.message);
                         setPredictionData(null); // Set to null if prediction fails
                    }
                }

                // Cache successful data
                const dataToCache = {
                    weatherData: weatherResponse.data,
                    aqiData: currentAqiData,
                    forecastData: forecastResponse.data.forecast,
                    predictionData: currentPredictionData,
                    timestamp: new Date().getTime(),
                };
                try {
                     localStorage.setItem(`weatherCache_${locationKey}`, JSON.stringify(dataToCache));
                     setIsOffline(false); // Successfully fetched online
                     setError(null); // Clear any previous errors
                     console.log("Successfully fetched and cached data for", locationKey);
                } catch (cacheError) {
                     console.error("Failed to write to localStorage cache:", cacheError);
                     setIsOffline(false); // Still online even if cache fails
                     setError(null); // Still a successful fetch
                }

            } catch (err) {
                 if (axios.isCancel(err)) return; // Ignore if request was cancelled
                 console.error("Error fetching weather data:", err);

                 // Attempt to load from cache on fetch failure
                 attemptLoadFromCache(locationKey, "Network or server error.");
            } finally {
                 // Only set loading to false here if initial cache wasn't used,
                 // otherwise loading was set to false already.
                 if (!usedInitialCache) {
                     setLoading(false);
                 }
            }
        };

         const attemptLoadFromCache = (key, baseErrorMessage) => {
             const cached = localStorage.getItem(`weatherCache_${key}`);
             if (cached) {
                 try {
                     const parsed = JSON.parse(cached);
                     // Check if cached data is still somewhat recent if possible, or just load it
                     // For simplicity, let's just load it if it exists after a failure
                     setWeatherData(parsed.weatherData);
                     setAqiData(parsed.aqiData);
                     setForecastData(parsed.forecastData);
                     setPredictionData(parsed.predictionData);
                     setIsOffline(true); // Using cached data due to failed fetch
                     setError(`${baseErrorMessage} Showing cached data.`);
                     console.log("Loaded cached data after fetch failure for", key);
                 } catch (e) {
                     console.error("Error parsing cache after failed fetch:", e);
                     setError("Network or server error. Failed to load cached data.");
                     setWeatherData(null);
                     setAqiData(null);
                     setForecastData(null);
                     setPredictionData(null);
                     setIsOffline(false); // No valid cache to fall back on
                 }
             } else {
                 // No cache available after failure
                 const finalErrorMessage = baseErrorMessage === "Network or server error." 
                    ? "New place detected. No data available offline." 
                    : `${baseErrorMessage} No cached data available.`;
                 setError(finalErrorMessage);
                 setWeatherData(null);
                 setAqiData(null);
                 setForecastData(null);
                 setPredictionData(null);
                 setIsOffline(false); // No cache, and fetch failed
             }
         };

        fetchData();

        // Cleanup function to cancel ongoing requests if location changes or component unmounts
        return () => {
            controller.abort();
        };

         // Added getLocationKey to dependency array because it's used inside the effect
    }, [location, getLocationKey]);

    return { weatherData, aqiData, forecastData, predictionData, loading, error, geoError, isOffline };
};

export default useWeatherData;