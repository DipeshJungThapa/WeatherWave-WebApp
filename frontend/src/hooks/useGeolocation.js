// src/hooks/useGeolocation.js
import { useState, useEffect } from 'react';

const useGeolocation = () => {
  const [location, setLocation] = useState(null); // Stores {lat, lon} if successful
  const [permissionDenied, setPermissionDenied] = useState(false); // True if permission is denied

  useEffect(() => {
    // Check if the browser supports geolocation
    if (!navigator.geolocation) {
      console.warn("Geolocation not supported by this browser.");
      // Optionally set an error state or permissionDenied here if you want to explicitly signal lack of support
      return;
    }

    // Request the current position
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        // Success callback: update location state
        setLocation({
          lat: pos.coords.latitude,
          lon: pos.coords.longitude
        });
        setPermissionDenied(false); // Ensure this is false on success
      },
      (err) => {
        // Error callback: handle permission denial or other errors
        console.error("Geolocation error:", err.message);
        if (err.code === 1) { // Error code 1 means permission denied
          setPermissionDenied(true);
        }
        setLocation(null); // Clear location on error
      },
      {
        // Optional: Options for getCurrentPosition
        enableHighAccuracy: false, // Less accurate, faster, less power consumption
        timeout: 5000,           // Max time to wait for location (5 seconds)
        maximumAge: 0            // Don't use a cached position
      }
    );
  }, []); // Empty dependency array means this effect runs once on mount

  return { location, permissionDenied };
};

export default useGeolocation;