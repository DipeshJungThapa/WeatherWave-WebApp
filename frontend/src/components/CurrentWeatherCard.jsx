// src/components/CurrentWeatherCard.jsx
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'; // Assuming Card components are in ui/

const CurrentWeatherCard = () => {
  return (
    <Card className="p-6 rounded-lg shadow-md">
      <CardHeader>
        <CardTitle className="text-xl font-semibold mb-2">Current City Weather</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Dummy data for now */}
        <p className="text-3xl font-bold mb-1">22°C <span className="text-xl font-normal">☁️ Partly Cloudy</span></p>
        <p className="text-md text-muted-foreground mb-4">Feels like 20°C</p>
        <div className="grid grid-cols-2 gap-y-2 text-sm">
          <p>💧 Humidity: 65%</p>
          <p>💨 Wind: 12 km/h</p>
          <p>👁️ Visibility: 10 km</p>
          <p> 압 Pressure: 1013 hPa</p>
        </div>
      </CardContent>
    </Card>
  );
};

export default CurrentWeatherCard;