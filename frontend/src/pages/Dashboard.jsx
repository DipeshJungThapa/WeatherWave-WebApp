// src/pages/Dashboard.jsx
import React from 'react';
// Import the new card components
import CurrentWeatherCard from '../components/CurrentWeatherCard';
import AQICard from '../components/AQICard';
import ForecastCard from '../components/ForecastCard';

const Dashboard = () => {
  // Remove unused state related to location selector (as it's now in Navbar)
  // const [openLocationPicker, setOpenLocationPicker] = React.useState(false);
  // const [selectedLocation, setSelectedLocation] = React.useState(null);
  // const { location, isLoading, getCurrentLocation } = useGeolocation();
  // Remove unused functions (as they are now in Navbar)
  // const handleLocationSelect = (location) => { ... };
  // React.useEffect(() => { ... }, [location]);

  return (
    <div className="flex min-h-[calc(100vh-64px)]">
      {/* Sidebar Section (unchanged) */}
      <aside className="w-64 bg-sidebar text-sidebar-foreground p-4 shadow-lg border-r border-sidebar-border">
        <h2 className="text-2xl font-semibold mb-6 text-sidebar-primary">Navigation</h2>
        <nav>
          <ul>
            <li className="mb-4">
              <a href="#" className="block p-2 rounded-md hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-colors duration-200">
                Current Weather
              </a>
            </li>
            <li className="mb-4">
              <a href="#" className="block p-2 rounded-md hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-colors duration-200">
                Forecast
              </a>
            </li>
            <li className="mb-4">
              <a href="#" className="block p-2 rounded-md hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-colors duration-200">
                Air Quality
              </a>
            </li>
            <li className="mb-4">
              <a href="#" className="block p-2 rounded-md hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-colors duration-200">
                Settings
              </a>
            </li>
          </ul>
        </nav>
        <div className="mt-8 pt-4 border-t border-sidebar-border">
            <p className="text-sm text-muted-foreground">Quick Links or Widgets</p>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 p-8 bg-background text-foreground">
        <h1 className="text-5xl font-extrabold mb-8 text-center">Welcome to WeatherWave Dashboard!</h1>
        <p className="text-lg text-center text-muted-foreground max-w-2xl mx-auto mb-8">
          Your personalized hub for real-time weather, forecasts, and air quality information.
          Use the sidebar for navigation and explore the data.
        </p>

        {/* Location Selector Section - REMOVED from here and moved to Navbar */}
        {/*
        <section className="mb-12 flex flex-col md:flex-row items-center justify-center space-y-4 md:space-y-0 md:space-x-4">
          // ... (Location Selector Popover and Button code was here) ...
        </section>
        */}

        {/* Grid for the three main weather information cards - NOW USING COMPONENTS */}
        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-12">
          {/* Replace the div placeholders with your new components */}
          <CurrentWeatherCard />
          <AQICard />
          <ForecastCard />
        </section>
      </div>
    </div>
  );
};

export default Dashboard;