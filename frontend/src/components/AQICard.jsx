// src/components/AQICard.jsx
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

const AQICard = () => {
  return (
    <Card className="p-6 rounded-lg shadow-md">
      <CardHeader>
        <CardTitle className="text-xl font-semibold mb-2">Air Quality Information</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Dummy data for now */}
        <p className="text-5xl font-bold text-center mb-2">85</p>
        <p className="text-lg font-medium text-center text-green-600 mb-4">Moderate</p>
        <p className="text-sm text-muted-foreground mb-4">
          Air quality is moderate. Sensitive individuals should consider limiting outdoor activities.
        </p>
        <div className="grid grid-cols-2 gap-y-2 text-sm">
          <p>PM2.5: 35 µg/m³</p>
          <p>PM10: 55 µg/m³</p>
          <p>O₃: 45 µg/m³</p>
          <p>NO₂: 25 µg/m³</p>
        </div>
      </CardContent>
    </Card>
  );
};

export default AQICard;