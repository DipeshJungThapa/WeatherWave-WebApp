// src/hooks/useWeatherData.js
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useDistrict } from '../context/DistrictContext';
import { useAuth } from '../context/AuthContext'; // <--- NEW IMPORT: useAuth hook

const useWeatherData = (latitude, longitude) => {
  const { district } = useDistrict();
  const { token } = useAuth(); // <--- NEW: Get token from AuthContext

  const [weather, setWeather] = useState(null);
  const [aqi, setAqi] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAllData = async () => {
      setLoading(true);
      setError(null);
      setWeather(null);
      setAqi(null);
      setPrediction(null);

      // Only fetch if a district or coordinates are available, AND if we have a token (or if token is not required yet)
      // For now, we fetch even without a token to see the 404s, but later backend will require it
      if (!district && (!latitude || !longitude)) {
          setLoading(false);
          return;
      }

      try {
        // Dynamically set headers: include Authorization if token exists
        const headers = token ? { Authorization: `Token ${token}` } : {}; // <--- NEW: Conditional Authorization header

        let locationPayload = {};

        if (latitude && longitude) {
          locationPayload = { latitude, longitude };
        } else if (district) {
          locationPayload = { city: district };
        } else {
          setLoading(false);
          setError("No location data (district or coordinates) available.");
          return;
        }

        const [weatherRes, aqiRes, predictRes] = await Promise.all([
          axios.get('/weather/', { headers, params: locationPayload }),
          axios.get('/aqi/', { headers, params: locationPayload }),
          axios.post('/predict/', locationPayload, { headers }),
        ]);

        setWeather(weatherRes.data);
        setAqi(aqiRes.data);
        setPrediction(predictRes.data.predicted_Temp_2m_tomorrow);

      } catch (err) {
        console.error("Error fetching data:", err);
        setError('Failed to fetch data.');
      } finally {
        setLoading(false);
      }
    };

    // Re-run effect when district, latitude, longitude, OR token changes
    fetchAllData();
  }, [district, latitude, longitude, token]); // <--- NEW: 'token' added to dependencies

  return { weather, aqi, prediction, loading, error };
};

export default useWeatherData;