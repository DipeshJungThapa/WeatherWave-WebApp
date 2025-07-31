// API configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

// API endpoints
export const API_ENDPOINTS = {
  CURRENT_WEATHER: '/api/current-weather/',
  FORECAST: '/api/forecast/',
  AQI: '/api/aqi/',
  PREDICT_CITY: '/api/predict-city/',
  ALERTS: '/api/alert/',
  FAVORITES: '/api/favorites/',
  REGISTER: '/register/',
  LOGIN: '/login/',
  USERS: '/users/',
  NEWS: '/api/news/',
  WEATHER_NEWS: '/api/weather-news/',
};

// Helper function to build full URL
export const buildApiUrl = (endpoint, params = '') => {
  const url = `${API_BASE_URL}${endpoint}`;
  return params ? `${url}?${params}` : url;
};
