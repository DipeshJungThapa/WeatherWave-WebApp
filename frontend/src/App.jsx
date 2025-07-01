import { useState } from 'react';
import './App.css';

function App() {
  const [location, setLocation] = useState('');
  const [weather, setWeather] = useState(null);

  // Placeholder for fetching weather data
  const fetchWeather = () => {
    // You will implement API call here
    setWeather({
      temp: '25°C',
      description: 'Sunny',
      humidity: '60%',
      wind: '10 km/h'
    });
  };

  return (
    <div className="app-container">
      <header>
        <h1>WeatherWave</h1>
      </header>
      <main>
        <div className="search-bar">
          <input
            type="text"
            placeholder="Enter city or district"
            value={location}
            onChange={e => setLocation(e.target.value)}
          />
          <button onClick={fetchWeather}>Get Weather</button>
        </div>
        {weather && (
          <div className="weather-card">
            <h2>{location}</h2>
            <p>Temperature: {weather.temp}</p>
            <p>Condition: {weather.description}</p>
            <p>Humidity: {weather.humidity}</p>
            <p>Wind: {weather.wind}</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;