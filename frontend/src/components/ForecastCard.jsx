// src/components/ForecastCard.jsx
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

const ForecastCard = () => {
  return (
    <Card className="p-6 rounded-lg shadow-md">
      <CardHeader>
        <CardTitle className="text-xl font-semibold mb-2">Upcoming Forecast</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Dummy data for now */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="font-semibold">Tuesday</span>
            <span className="text-muted-foreground">🌤️ 24°C / 15°C</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="font-semibold">Wednesday</span>
            <span className="text-muted-foreground">🌧️ 20°C / 12°C</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="font-semibold">Thursday</span>
            <span className="text-muted-foreground">☀️ 28°C / 18°C</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="font-semibold">Friday</span>
            <span className="text-muted-foreground">☁️ 23°C / 14°C</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="font-semibold">Saturday</span>
            <span className="text-muted-foreground">⛈️ 25°C / 16°C</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ForecastCard;