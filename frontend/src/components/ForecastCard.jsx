// frontend/src/components/ForecastCard.jsx
import React from 'react';
import { motion } from 'framer-motion';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from './ui/card';
import {
  CalendarDays,
  ArrowUp,
  ArrowDown,
  CloudSun,
  CloudRain,
  Sun,
  Cloud,
  Snowflake,
} from 'lucide-react';

function ForecastCard({ data, unit }) {
  if (!data || !Array.isArray(data) || data.length === 0) {
    return (
      <Card className="flex flex-col items-center justify-center p-4">
        <CardHeader>
          <CardTitle>5-Day Forecast</CardTitle>
        </CardHeader>
        <CardContent>
          <p>No forecast data available.</p>
        </CardContent>
      </Card>
    );
  }

  // Helper function to pick an icon based on description or fallback
  const getWeatherIcon = (description = '') => {
    const desc = description.toLowerCase();
    if (desc.includes('rain')) return <CloudRain className="h-5 w-5 text-blue-500" />;
    if (desc.includes('cloud')) return <Cloud className="h-5 w-5 text-gray-500" />;
    if (desc.includes('sun')) return <Sun className="h-5 w-5 text-yellow-500" />;
    if (desc.includes('snow')) return <Snowflake className="h-5 w-5 text-cyan-500" />;
    return <CloudSun className="h-5 w-5 text-indigo-500" />; // Default icon
  };

  return (
    <Card className="w-full h-full flex flex-col justify-between p-6 overflow-hidden">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">5-Day Forecast</CardTitle>
        <CardDescription className="text-muted-foreground">
          Daily average, min, and max temperatures
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {data.map((day, index) => (
          <motion.div
            key={index}
            whileHover={{ scale: 1.02 }}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2, delay: index * 0.1 }}
            className="flex items-center justify-between rounded-lg bg-muted px-3 py-2"
          >
            <div className="flex items-center space-x-2">
              <CalendarDays className="h-4 w-4 text-muted-foreground" />
              <span className="font-medium whitespace-nowrap">
                {new Date(day.date).toLocaleDateString('en-GB', {
                  weekday: 'short',
                  day: '2-digit',
                  month: 'short',
                })}
              </span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="flex items-center text-sm">
                <ArrowUp className="h-4 w-4 text-red-500 mr-1" />
                <span>{unit === 'Celsius' ? `${day.Weather.max_temp.toFixed(1)}°C` : `${(day.Weather.max_temp * 9/5 + 32).toFixed(1)}°F`}</span>
              </div>
              <div className="flex items-center text-sm">
                <ArrowDown className="h-4 w-4 text-blue-500 mr-1" />
                <span>{unit === 'Celsius' ? `${day.Weather.min_temp.toFixed(1)}°C` : `${(day.Weather.min_temp * 9/5 + 32).toFixed(1)}°F`}</span>
              </div>
              <div className="text-sm font-semibold">
                {unit === 'Celsius' ? `${day.Weather.avg_temp.toFixed(1)}°C` : `${(day.Weather.avg_temp * 9/5 + 32).toFixed(1)}°F`}
              </div>
              {getWeatherIcon(day.Weather.description)}
            </div>
          </motion.div>
        ))}
      </CardContent>
    </Card>
  );
}

export default ForecastCard;
