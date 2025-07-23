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
      <Card className="flex flex-col items-center justify-center p-4 bg-white/30 dark:bg-black/30 backdrop-blur-md">
        <CardHeader>
          <CardTitle>5-Day Forecast</CardTitle>
        </CardHeader>
        <CardContent>
          <p>No forecast data available.</p>
        </CardContent>
      </Card>
    );
  }

  const getWeatherIcon = (description = '') => {
    const desc = description.toLowerCase();
    if (desc.includes('rain')) return <CloudRain className="h-4 w-4 text-blue-500" />;
    if (desc.includes('cloud')) return <Cloud className="h-4 w-4 text-gray-500" />;
    if (desc.includes('sun')) return <Sun className="h-4 w-4 text-yellow-500" />;
    if (desc.includes('snow')) return <Snowflake className="h-4 w-4 text-cyan-500" />;
    return <CloudSun className="h-4 w-4 text-indigo-500" />;
  };

  return (
    <Card className="w-full flex flex-col p-4 bg-white/30 dark:bg-black/30 backdrop-blur-md min-h-[270px]">
      <CardHeader className="pb-2">
        <CardTitle className="text-xl font-bold">5-Day Forecast</CardTitle>
        <CardDescription className="text-sm text-muted-foreground">
          Daily average, min, and max temperatures
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-2 px-1 pb-2">
        {data.slice(0, 5).map((day, index) => (
          <motion.div
            key={index}
            whileHover={{ scale: 1.01 }}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2, delay: index * 0.05 }}
            className="flex items-center justify-between rounded-md bg-muted px-2 py-1 text-sm"
          >
            <div className="flex items-center space-x-2 w-32 min-w-[100px]">
              <CalendarDays className="h-4 w-4 text-muted-foreground" />
              <span className="whitespace-nowrap">
                {new Date(day.date).toLocaleDateString('en-GB', {
                  weekday: 'short',
                  day: '2-digit',
                  month: 'short',
                })}
              </span>
            </div>

            <div className="flex items-center gap-3 text-xs">
              <div className="flex items-center">
                <ArrowUp className="h-3.5 w-3.5 text-red-500 mr-1" />
                <span>
                  {unit === 'Celsius'
                    ? `${day.Weather.max_temp.toFixed(1)}°C`
                    : `${(day.Weather.max_temp * 9 / 5 + 32).toFixed(1)}°F`}
                </span>
              </div>
              <div className="flex items-center">
                <ArrowDown className="h-3.5 w-3.5 text-blue-500 mr-1" />
                <span>
                  {unit === 'Celsius'
                    ? `${day.Weather.min_temp.toFixed(1)}°C`
                    : `${(day.Weather.min_temp * 9 / 5 + 32).toFixed(1)}°F`}
                </span>
              </div>
              <div className="font-semibold">
                {unit === 'Celsius'
                  ? `${day.Weather.avg_temp.toFixed(1)}°C`
                  : `${(day.Weather.avg_temp * 9 / 5 + 32).toFixed(1)}°F`}
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
