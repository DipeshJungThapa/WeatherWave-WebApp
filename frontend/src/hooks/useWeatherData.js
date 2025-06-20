// src/hooks/useWeatherData.js
import { useEffect, useState } from 'react';
import { useDistrict } from '../context/DistrictContext'; // <--- Now imports our custom useDistrict hook
import axios from 'axios';

export default function useWeatherData() {
  const { district } = useDistrict(); // Get the selected district from our global context
  const [data, setData] = useState({
    weather: null,
    aqi: null,
    prediction: null,
    loading: true, // Indicates if data is currently being fetched
    error: null,   // Stores any error message
  });

  useEffect(() => {
    // Only fetch if a district is selected
    if (!district) {
      setData(prev => ({ ...prev, loading: false, error: null })); // If no district, not loading, no error
      return;
    }

    const fetchData = async () => {
      setData(prev => ({ ...prev, loading: true, error: null })); // Start loading, clear previous error
      try {
        // These are your *future* backend API endpoints
        const [weatherRes, predictionRes] = await Promise.all([
          axios.get(`/api/live-weather?district=${district}`), // Example: /api/live-weather?district=Kathmandu
          axios.post(`/api/predict`, { district }),            // Example: /api/predict with { district: "Kathmandu" }
        ]);

        // Assuming AQI might come within the weather response
        const aqi = weatherRes.data.aqi ?? null; // Use null if AQI is not provided

        setData({
          weather: weatherRes.data,
          prediction: predictionRes.data.predicted_Temp_2m_tomorrow, // Assuming this is the exact key
          aqi,
          loading: false, // Done loading
          error: null,    // No error
        });
      } catch (error) {
        console.error("Error fetching weather data:", error);
        setData({
          weather: null, aqi: null, prediction: null,
          loading: false, // Done loading, but with an error
          error: error.message || 'Failed to fetch data', // Capture error message
        });
      }
    };

    fetchData();
  }, [district]); // Re-run this effect whenever the 'district' changes

  return data; // Return the current state of data, loading, and error
}