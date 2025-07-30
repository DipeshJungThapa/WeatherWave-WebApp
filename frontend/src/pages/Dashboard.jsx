// src/pages/Dashboard.jsx
import React, { useState, useEffect, useCallback } from 'react';
import useWeatherData from "../hooks/useWeatherData";
import CurrentWeatherCard from "../components/CurrentWeatherCard";
import AQICard from "../components/AQICard";
import ForecastCard from "../components/ForecastCard";
import PredictionCard from "../components/PredictionCard";
import NepalWeatherHeatmap from "../components/ZoomEarthHeatmap";
import WeatherNews from "../components/WeatherNews";

import { Alert, AlertDescription, AlertTitle } from "../components/ui/alert";
import { Skeleton } from "../components/ui/skeleton";
import { Button } from "../components/ui/button";
import { Heart, WifiOff, AlertTriangle, CloudAlert } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Dashboard({ currentDistrict, unit }) {
    const { isAuthenticated, token } = useAuth();

    const {
        weatherData,
        aqiData,
        forecastData,
        predictionData,
        loading,
        error,
        geoError,
        isOffline
    } = useWeatherData(currentDistrict);

    const [isFavorited, setIsFavorited] = useState(false);
    const [currentFavoriteId, setCurrentFavoriteId] = useState(null);
    const [weatherAlerts, setWeatherAlerts] = useState([]);
    const [alertsLoading, setAlertsLoading] = useState(false);
    const [alertsError, setAlertsError] = useState(null);

    // Fetch weather alerts from backend API
    const fetchWeatherAlerts = useCallback(async (city) => {
        if (!city || isOffline) return;
        
        setAlertsLoading(true);
        setAlertsError(null);
        
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/alert/?city=${encodeURIComponent(city)}`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                const data = await response.json();
                setWeatherAlerts(data.alerts || []);
            } else {
                setAlertsError('Failed to fetch weather alerts');
                setWeatherAlerts([]);
            }
        } catch (err) {
            console.error('Weather alerts fetch error:', err);
            setAlertsError('Unable to load weather alerts');
            setWeatherAlerts([]);
        } finally {
            setAlertsLoading(false);
        }
    }, [isOffline]);

    // Fetch alerts when weather data or district changes
    useEffect(() => {
        const city = weatherData?.city || currentDistrict;
        if (city && !isOffline) {
            fetchWeatherAlerts(city);
        }
    }, [weatherData?.city, currentDistrict, fetchWeatherAlerts, isOffline]);

    const checkIfFavorited = useCallback(async (cityToCheck) => {
        if (!token || typeof cityToCheck !== 'string' || !cityToCheck) {
            setIsFavorited(false);
            setCurrentFavoriteId(null);
            return;
        }

        // Only attempt to fetch favorites if online
        if (isOffline) {
             setIsFavorited(false);
             setCurrentFavoriteId(null);
             return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/api/favorites/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                },
            });

            if (response.ok) {
                const favorites = await response.json();
                const found = favorites.find(fav => fav.city_name.toLowerCase() === cityToCheck.toLowerCase());
                setIsFavorited(!!found);
                setCurrentFavoriteId(found ? found.id : null);
            } else {
                setIsFavorited(false);
                setCurrentFavoriteId(null);
            }
        } catch (err) {
            console.error("Error checking favorites:", err);
            setIsFavorited(false);
            setCurrentFavoriteId(null);
        }
    }, [token, isOffline]); // Add isOffline to dependency array

    useEffect(() => {
        const cityString = weatherData?.city || (typeof currentDistrict === 'string' ? currentDistrict : null);
        // Only check favorites if online or if we have weather data (which might be from cache initially)
        if ((!isOffline && cityString && token) || (weatherData && token)) {
            checkIfFavorited(cityString);
        }
    }, [currentDistrict, token, weatherData?.city, checkIfFavorited, isOffline]); // Add isOffline to dependency array

    const handleToggleFavorite = async () => {
        if (!token) return alert("Please login to manage favorites.");
        if (isOffline) return alert("Cannot manage favorites while offline."); // Prevent favorite actions when offline

        const city = weatherData?.city || currentDistrict;
        if (!city) return alert("No valid city selected.");

        if (isFavorited) {
            try {
                const res = await fetch(`http://127.0.0.1:8000/api/favorites/${currentFavoriteId}/`, {
                    method: 'DELETE',
                    headers: { 'Authorization': `Token ${token}` }
                });
                if (res.status === 204) {
                    setIsFavorited(false);
                    setCurrentFavoriteId(null);
                    alert(`${city} removed from favorites.`);
                } else {
                     // Handle potential errors even if status is not 204
                     alert("Error removing favorite.");
                }
            } catch (err) {
                alert("Error removing favorite.");
            }
        } else {
            try {
                const res = await fetch('http://127.0.0.1:8000/api/favorites/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${token}`
                    },
                    body: JSON.stringify({ city_name: city })
                });
                if (res.ok) {
                    const data = await res.json();
                    setIsFavorited(true);
                    setCurrentFavoriteId(data.id);
                    alert(`${city} added to favorites.`);
                } else {
                    const errorData = await res.json();
                    if (errorData.non_field_errors?.includes("The fields user, city_name must make a unique set.")) {
                        setIsFavorited(true);
                        alert(`${city} is already in your favorites.`);
                        checkIfFavorited(city); // Recheck to get ID
                    } else {
                         // Handle other potential errors
                         alert("Error adding to favorites.");
                    }
                }
            } catch (err) {
                alert("Error adding to favorites.");
            }
        }
    };

    const dashboardTitleLocation = typeof currentDistrict === 'string'
        ? currentDistrict
        : (currentDistrict?.latitude ? 'Current Location' : 'Selected Location');

    // Loading state handling (remains the same)
    if (loading && !isOffline) { // Only show skeleton loading if truly loading (not just displaying cache)
        return (
            <div className="container mx-auto p-6">
                <Alert className="mb-6">
                    <AlertTitle>Loading...</AlertTitle>
                    <AlertDescription>Fetching weather data for {dashboardTitleLocation}...</AlertDescription>
                </Alert>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {[...Array(4)].map((_, i) => <Skeleton key={i} className="h-[200px] w-full" />)}
                </div>
            </div>
        );
    }

     // If loading but offline, we might be loading the cache, show a different message or the existing data
    if (loading && isOffline) {
         return (
             <div className="container mx-auto p-6">
                 <Alert className="mb-6 bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200">
                     <WifiOff className="h-4 w-4" />
                     <AlertTitle>Offline Mode</AlertTitle>
                     <AlertDescription>Attempting to fetch data, showing cached data...</AlertDescription>
                 </Alert>
                 {/* Optionally show skeleton or just the old data while attempting to refresh */}
                 {/* Display existing data if available while trying to refresh */}
                 {weatherData || aqiData || forecastData || predictionData ? (
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                          {weatherData && <CurrentWeatherCard data={weatherData} unit={unit} currentCity={currentDistrict} />}
                          {aqiData && <AQICard data={aqiData} />}
                          {forecastData && <ForecastCard data={forecastData} unit={unit} />}
                          <PredictionCard data={predictionData} unit={unit} />
                      </div>
                 ) : (
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                           {[...Array(4)].map((_, i) => <Skeleton key={i} className="h-[200px] w-full" />)}
                      </div>
                 )}
             </div>
         );
    }


    // Geolocation error fallback (remains the same, but check for isOffline to potentially show cached data)
    if (geoError) {
        return (
            <div className="container mx-auto p-6 space-y-6">
                <Alert variant="warning">
                    <AlertTriangle className="h-4 w-4" />
                    <AlertTitle>Location Error</AlertTitle>
                    <AlertDescription>
                        {geoError}. Please enable location services or select a district.
                    </AlertDescription>
                </Alert>
                 {/* Show cached data if available even with geo error */}
                {isOffline && (weatherData || aqiData || forecastData || predictionData) && (
                    <>
                         <Alert className="bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200">
                             <WifiOff className="h-4 w-4" />
                             <AlertTitle>Offline Mode</AlertTitle>
                             <AlertDescription>Showing cached data (offline or network issue).</AlertDescription>
                         </Alert>
                         <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                              {weatherData && <CurrentWeatherCard data={weatherData} unit={unit} currentCity={currentDistrict} />}
                              {aqiData && <AQICard data={aqiData} />}
                              {forecastData && <ForecastCard data={forecastData} unit={unit} />}
                              <PredictionCard data={predictionData} unit={unit} />
                         </div>
                    </>
                 )}
            </div>
        );
    }

    // If not loading and no geo error, display data or general error
    if (error && !isOffline && !weatherData && !aqiData && !forecastData && !predictionData) { // Show general error only if no data (cached or new) and not offline mode showing cache
        return (
             <div className="container mx-auto p-6 space-y-6">
                 <Alert variant="destructive" className="mb-4">
                     <AlertTriangle className="h-4 w-4" />
                     <AlertTitle>Error</AlertTitle>
                     <AlertDescription>{error}</AlertDescription>
                 </Alert>
             </div>
        );
    }

    // Main display when data is available (either live or cached)
    return (
        
        <div className="container mx-auto p-6 space-y-6">
            {/* Weather Alerts Section */}
            <div className="mb-4">
                {alertsLoading ? (
                    <Alert className="bg-blue-50 border-blue-200">
                        <CloudAlert className="h-4 w-4 text-blue-600" />
                        <AlertTitle className="text-blue-800">Loading Weather Alerts...</AlertTitle>
                        <AlertDescription className="text-blue-700">
                            Checking for active weather warnings...
                        </AlertDescription>
                    </Alert>
                ) : alertsError ? (
                    <Alert className="bg-yellow-50 border-yellow-200">
                        <AlertTriangle className="h-4 w-4 text-yellow-600" />
                        <AlertTitle className="text-yellow-800">Weather Alerts Unavailable</AlertTitle>
                        <AlertDescription className="text-yellow-700">
                            {alertsError}
                        </AlertDescription>
                    </Alert>
                ) : weatherAlerts.length > 0 ? (
                    <div className="space-y-2">
                        {weatherAlerts.map((alert, index) => (
                            <Alert 
                                key={index} 
                                className={`
                                    ${alert.severity === 'severe' ? 'bg-red-50 border-red-200' : 
                                      alert.severity === 'moderate' ? 'bg-orange-50 border-orange-200' : 
                                      'bg-yellow-50 border-yellow-200'}
                                `}
                            >
                                <AlertTriangle className={`h-4 w-4 ${
                                    alert.severity === 'severe' ? 'text-red-600' : 
                                    alert.severity === 'moderate' ? 'text-orange-600' : 
                                    'text-yellow-600'
                                }`} />
                                <AlertTitle className={`
                                    ${alert.severity === 'severe' ? 'text-red-800' : 
                                      alert.severity === 'moderate' ? 'text-orange-800' : 
                                      'text-yellow-800'}
                                `}>
                                    {alert.event || 'Weather Alert'}
                                </AlertTitle>
                                <AlertDescription className={`
                                    ${alert.severity === 'severe' ? 'text-red-700' : 
                                      alert.severity === 'moderate' ? 'text-orange-700' : 
                                      'text-yellow-700'}
                                `}>
                                    {alert.description || alert.title}
                                    {alert.effective && (
                                        <div className="mt-1 text-xs">
                                            Effective: {new Date(alert.effective).toLocaleString()}
                                        </div>
                                    )}
                                </AlertDescription>
                            </Alert>
                        ))}
                    </div>
                ) : (
                    <Alert className="bg-green-50 border-green-200">
                        <CloudAlert className="h-4 w-4 text-green-600" />
                        <AlertTitle className="text-green-800">No Active Weather Alerts</AlertTitle>
                        <AlertDescription className="text-green-700">
                            No weather warnings currently active for {weatherData?.city || currentDistrict}.
                        </AlertDescription>
                    </Alert>
                )}
            </div>
            {/* Offline Mode Info */}
            {isOffline && (
                <Alert className="mb-4 bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200">
                    <WifiOff className="h-4 w-4" />
                    <AlertTitle>Offline Mode</AlertTitle>
                    <AlertDescription>{error || "Showing cached data (offline or network issue)."}</AlertDescription>
                </Alert>
            )}

            {/* General Error when NOT offline and NO data */}
             {error && !isOffline && !weatherData && !aqiData && !forecastData && !predictionData && (
                 <Alert variant="destructive" className="mb-4">
                     <AlertTriangle className="h-4 w-4" />
                     <AlertTitle>Error</AlertTitle>
                     <AlertDescription>{error}</AlertDescription>
                 </Alert>
             )}

            <div className="bg-white/30 dark:bg-black/30 backdrop-blur-md p-6 rounded-2xl space-y-6">
                <div className="flex justify-between items-center">
                    <h1 className="text-3xl font-bold">Weather Dashboard for "{dashboardTitleLocation}"</h1>
                    {isAuthenticated && weatherData?.city && !isOffline && ( // Disable favorite button when offline
                        <Button variant="outline" onClick={handleToggleFavorite} className="flex items-center space-x-2">
                            <Heart className={`h-5 w-5 ${isFavorited ? 'text-red-500 fill-red-500' : 'text-muted-foreground'}`} />
                            <span>{isFavorited ? 'Favorited' : 'Add to Favorites'}</span>
                        </Button>
                    )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {/* Render cards only if data is available */}
                    {weatherData && <CurrentWeatherCard data={weatherData} unit={unit} currentCity={currentDistrict} />}
                    {aqiData && <AQICard data={aqiData} />}
                    {forecastData && <ForecastCard data={forecastData} unit={unit} />}
                    {predictionData && <PredictionCard data={predictionData} unit={unit} />}

                     {/* Display a message if no data is available (neither live nor cached) */}
                     {!weatherData && !aqiData && !forecastData && !predictionData && (
                          <div className="col-span-full text-center text-muted-foreground">
                              No weather data available for this location.
                          </div>
                     )}
                </div>
            </div>

            {/* Heatmap at the bottom */}
            <div>
                 {isOffline && (
                     <Alert className="mb-4 bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200">
                         <WifiOff className="h-4 w-4" />
                         <AlertTitle>Heatmap Offline</AlertTitle>
                         <AlertDescription>Live heatmap is not available in offline mode.</AlertDescription>
                     </Alert>
                 )}
                 {/* Only show heatmap iframe if online */}
                 {!isOffline && <NepalWeatherHeatmap />}
            </div>

            {/* Weather News Section */}
            <div>
                <WeatherNews />
            </div>
        </div>
    );
}
