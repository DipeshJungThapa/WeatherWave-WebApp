// src/pages/Dashboard.jsx
import React, { useState, useEffect, useCallback } from 'react';
import useWeatherData from "../hooks/useWeatherData";
import CurrentWeatherCard from "../components/CurrentWeatherCard";
import AQICard from "../components/AQICard";
import ForecastCard from "../components/ForecastCard";
import PredictionCard from "../components/PredictionCard";
import { Alert, AlertDescription, AlertTitle } from "../components/ui/alert";
import { Skeleton } from "../components/ui/skeleton";
import { Button } from "../components/ui/button";
import { Heart } from 'lucide-react';
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
        geoError
    } = useWeatherData(currentDistrict);

    const [isFavorited, setIsFavorited] = useState(false);
    const [currentFavoriteId, setCurrentFavoriteId] = useState(null);

    // Function to check if the current city is favorited
    const checkIfFavorited = useCallback(async (cityToCheck) => {
        // Only check favorites if user is authenticated and has a token
        if (!isAuthenticated || !token || typeof cityToCheck !== 'string' || !cityToCheck) {
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
                const foundFavorite = favorites.find(fav => fav.city_name.toLowerCase() === cityToCheck.toLowerCase());
                setIsFavorited(!!foundFavorite);
                setCurrentFavoriteId(foundFavorite ? foundFavorite.id : null);
            } else if (response.status === 401) {
                console.log('User not authenticated for favorites');
                setIsFavorited(false);
                setCurrentFavoriteId(null);
            } else {
                console.error('Failed to fetch favorites for check:', response.status);
                setIsFavorited(false);
                setCurrentFavoriteId(null);
            }
        } catch (error) {
            console.error('Network error checking favorites:', error);
            setIsFavorited(false);
            setCurrentFavoriteId(null);
        }
    }, [token, isAuthenticated]);

    // Effect to run checkIfFavorited when currentDistrict or resolved city name changes
    useEffect(() => {
        // Only check if user is authenticated
        if (isAuthenticated && token) {
            const cityString = weatherData?.city || (typeof currentDistrict === 'string' ? currentDistrict : null);
            if (cityString) {
                checkIfFavorited(cityString);
            }
        } else {
            setIsFavorited(false);
            setCurrentFavoriteId(null);
        }
    }, [currentDistrict, token, weatherData?.city, checkIfFavorited, isAuthenticated]);

    // Function to toggle favorite status (add/remove)
    const handleToggleFavorite = async () => {
        if (!isAuthenticated || !token) {
            alert("You must be logged in to manage favorites!");
            return;
        }

        // Use the city name from weatherData if available, otherwise from currentDistrict if it's a string
        const cityToManage = weatherData?.city || (typeof currentDistrict === 'string' ? currentDistrict : null);
        if (!cityToManage) {
            alert("No city selected to manage favorite status!");
            return;
        }

        if (isFavorited) {
            // Logic to REMOVE from favorites
            if (!currentFavoriteId) {
                console.error("Attempted to unfavorite but no ID found. Re-checking favorite status...");
                await checkIfFavorited(cityToManage);
                if (!currentFavoriteId) {
                    alert("Error: Could not unfavorite. Please try again.");
                    return;
                }
            }

            try {
                const response = await fetch(`http://127.0.0.1:8000/api/favorites/${currentFavoriteId}/`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Token ${token}`,
                    },
                });

                if (response.status === 204) {
                    console.log('Favorite removed successfully!');
                    setIsFavorited(false);
                    setCurrentFavoriteId(null);
                    alert(`${cityToManage} removed from favorites!`);
                } else if (response.status === 404) {
                    alert(`${cityToManage} not found in your favorites or already removed.`);
                    setIsFavorited(false);
                    setCurrentFavoriteId(null);
                } else {
                    const errorData = await response.json();
                    console.error('Failed to remove favorite:', response.status, errorData);
                    alert(`Failed to remove favorite: ${response.status} - ${JSON.stringify(errorData)}`);
                }
            } catch (error) {
                console.error('Network error or unexpected error during favorite removal:', error);
                alert('An unexpected error occurred while removing favorite.');
            }
        } else {
            // Logic to ADD to favorites
            const favoriteData = {
                city_name: cityToManage,
            };

            try {
                const response = await fetch('http://127.0.0.1:8000/api/favorites/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${token}`,
                    },
                    body: JSON.stringify(favoriteData),
                });

                if (response.ok) {
                    const responseData = await response.json();
                    console.log('Favorite added successfully:', responseData);
                    setIsFavorited(true);
                    setCurrentFavoriteId(responseData.id);
                    alert(`${cityToManage} added to favorites!`);
                } else if (response.status === 400) {
                    const errorData = await response.json();
                    if (errorData.non_field_errors && errorData.non_field_errors.includes('The fields user, city_name must make a unique set.')) {
                        alert(`${cityToManage} is already in your favorites!`);
                        setIsFavorited(true);
                        checkIfFavorited(cityToManage);
                    } else {
                        console.error('Error adding favorite (400):', errorData);
                        alert(`Failed to add favorite: ${JSON.stringify(errorData)}`);
                    }
                } else {
                    const errorData = await response.json();
                    console.error('Failed to add favorite:', response.status, errorData);
                    alert(`Failed to add favorite: ${response.status} - ${JSON.stringify(errorData)}`);
                }
            } catch (error) {
                console.error('Network error or unexpected error during favorite add:', error);
                alert('An unexpected error occurred while adding favorite.');
            }
        }
    };

    // Determine the display name for the dashboard header
    const dashboardTitleLocation = typeof currentDistrict === 'string'
        ? currentDistrict
        : (currentDistrict && currentDistrict.latitude ? 'Current Location' : 'Selected Location');

    // Loading state
    if (loading) {
        return (
            <div className="container mx-auto p-6">
                <Alert className="mb-6">
                    <AlertTitle>Loading...</AlertTitle>
                    <AlertDescription>
                        Fetching weather data for {dashboardTitleLocation}.
                    </AlertDescription>
                </Alert>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <Skeleton className="h-[200px] w-full" />
                    <Skeleton className="h-[200px] w-full" />
                    <Skeleton className="h-[200px] w-full" />
                    <Skeleton className="h-[200px] w-full" />
                </div>
            </div>
        );
    }

    // Error state
    if (error) {
        return (
            <div className="container mx-auto p-6">
                <Alert variant="destructive">
                    <AlertTitle>Error!</AlertTitle>
                    <AlertDescription>{error}</AlertDescription>
                </Alert>
            </div>
        );
    }

    // Geolocation error fallback
    if (geoError) {
        return (
            <div className="container mx-auto p-6 space-y-6">
                <Alert variant="warning">
                    <AlertTitle>Location Error</AlertTitle>
                    <AlertDescription>
                        {geoError}. Please enable location services or select a district from the dropdown.
                    </AlertDescription>
                </Alert>
                <div className="flex justify-between items-center">
                    <h1 className="text-3xl font-bold text-foreground">Weather Dashboard for "{dashboardTitleLocation}"</h1>
                    {isAuthenticated && weatherData?.city && (
                        <Button variant="outline" onClick={handleToggleFavorite} className="flex items-center space-x-2">
                            <Heart className={`h-5 w-5 ${isFavorited ? 'text-red-500 fill-red-500' : 'text-muted-foreground'}`} />
                            <span>{isFavorited ? 'Favorited' : 'Add to Favorites'}</span>
                        </Button>
                    )}
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-6">
                    {weatherData && <CurrentWeatherCard data={weatherData} unit={unit} currentCity={currentDistrict} />}
                    {aqiData && <AQICard data={aqiData} />}
                    {forecastData && <ForecastCard data={forecastData} unit={unit} />}
                    <PredictionCard data={predictionData} />
                </div>
            </div>
        );
    }

    // Main content
    return (
        <div className="container mx-auto p-6 space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold text-foreground">Weather Dashboard for "{dashboardTitleLocation}"</h1>
                {isAuthenticated && weatherData?.city && (
                    <Button variant="outline" onClick={handleToggleFavorite} className="flex items-center space-x-2">
                        <Heart className={`h-5 w-5 ${isFavorited ? 'text-red-500 fill-red-500' : 'text-muted-foreground'}`} />
                        <span>{isFavorited ? 'Favorited' : 'Add to Favorites'}</span>
                    </Button>
                )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {weatherData && <CurrentWeatherCard data={weatherData} unit={unit} currentCity={currentDistrict} />}
                {aqiData && <AQICard data={aqiData} />}
                {forecastData && <ForecastCard data={forecastData} unit={unit} />}
                <PredictionCard data={predictionData} />
            </div>
        </div>
    );
}