// src/components/CurrentWeatherCard.jsx
import React, { useEffect } from 'react'; // Import useEffect for console.log
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from './ui/card';
import { Thermometer, Droplet, Wind } from 'lucide-react';

export default function CurrentWeatherCard({ data, currentCity, unit }) { // Added unit prop
  // Add a console log to see what data is being received
  useEffect(() => {
    console.log("CurrentWeatherCard received data:", data);
    console.log("CurrentWeatherCard received currentCity prop:", currentCity);
    console.log("CurrentWeatherCard received unit prop:", unit);
  }, [data, currentCity, unit]);


  if (!data) {
    return (
      <Card className="hover:shadow-lg transition-shadow bg-white/30 dark:bg-black/30 backdrop-blur-md">
        <CardHeader>
          <CardTitle>No Data</CardTitle>
        </CardHeader>
        <CardContent>
          <p>No current weather available.</p>
        </CardContent>
      </Card>
    );
  }

  // MODIFIED LINE BELOW:
  let displayCity;
  // If currentCity is an object with latitude and longitude (from "Use Location")
  if (currentCity && typeof currentCity === 'object' && currentCity.latitude && currentCity.longitude) {
      displayCity = 'Current Location';
  } 
  // Otherwise, if data.city is available from the API response
  else if (data.city) {
      displayCity = data.city;
  } 
  // Otherwise, if currentCity is a string (from dropdown selection)
  else if (typeof currentCity === 'string') {
      displayCity = currentCity;
  } 
  // Fallback if no specific location can be determined
  else {
      displayCity = 'Unknown Location';
  }

  const temperature = unit === 'Celsius' ? `${Math.round(data.temp)}°C` : `${Math.round(data.temp * 9/5 + 32)}°F`; // Convert temperature based on unit

  return (
    <Card className="hover:shadow-lg transition-shadow flex flex-col justify-between bg-white/30 dark:bg-black/30 backdrop-blur-md">
      <CardHeader>
        <CardTitle className="text-xl">{displayCity}</CardTitle>
        <p className="text-sm text-muted-foreground capitalize">{data.description}</p>
      </CardHeader>

      <CardContent className="flex flex-col items-center space-y-2">
        <div className="flex items-center space-x-2 text-5xl font-extrabold">
          <Thermometer className="h-8 w-8 text-primary" />
          <span>{temperature}</span>
        </div>
      </CardContent>

      <CardFooter className="flex justify-around pt-4 text-sm text-muted-foreground">
        <div className="flex flex-col items-center">
          <Droplet className="h-5 w-5 text-blue-500" />
          <span>{data.humidity}%</span>
          <span>Humidity</span>
        </div>
        <div className="flex flex-col items-center">
          <Wind className="h-5 w-5 text-blue-500" />
          <span>{data.wind_speed.toFixed(1)} m/s</span>
          <span>Wind</span>
        </div>
      </CardFooter>
    </Card>
  );
}
