// src/hooks/useGeolocation.js
import { useState, useEffect } from 'react';

const useGeolocation = () => {
  const [location, setLocation] = useState({
    latitude: null,
    longitude: null,
    error: null,
  });

  const [isLoading, setIsLoading] = useState(false);

  const successHandler = (position) => {
    setLocation({
      latitude: position.coords.latitude,
      longitude: position.coords.longitude,
      error: null,
    });
    setIsLoading(false);
  };

  const errorHandler = (geoError) => {
    setLocation((prev) => ({
      ...prev,
      error: geoError.message,
    }));
    setIsLoading(false);
    console.error("Geolocation error:", geoError.message);
  };

  const getCurrentLocation = () => {
    if (!navigator.geolocation) {
      setLocation((prev) => ({
        ...prev,
        error: "Geolocation is not supported by your browser.",
      }));
      return;
    }

    setIsLoading(true);
    navigator.geolocation.getCurrentPosition(successHandler, errorHandler, {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0,
    });
  };

  // Optional: You might want to get location on mount, or only on button click
  // For this plan, we'll trigger it on button click.
  // useEffect(() => {
  //   getCurrentLocation();
  // }, []);

  return { location, isLoading, getCurrentLocation };
};

export default useGeolocation;