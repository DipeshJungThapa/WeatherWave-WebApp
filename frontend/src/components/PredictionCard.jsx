// src/components/PredictionCard.jsx
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card'; // Adjust path to shadcn/ui Card
import { Alert, AlertDescription, AlertTitle } from './ui/alert'; // Adjust path to shadcn/ui Alert
import { Badge } from './ui/badge'; // Adjust path to shadcn/ui Badge
import { useTheme } from 'next-themes'; // Import useTheme hook

const PredictionCard = ({ data, unit }) => { // Added unit prop
  const { theme } = useTheme(); // Get current theme

  if (!data || !data.predicted_temp) {
    return (
      <Card className="bg-white/30 dark:bg-black/30 backdrop-blur-md">
        <CardHeader>
          <CardTitle>ML Prediction</CardTitle>
        </CardHeader>
        <CardContent>
          <p>No prediction data available.</p>
        </CardContent>
      </Card>
    );
  }

  // Convert temperature based on unit prop
  const temperature = unit === 'Celsius' 
    ? `${Math.round(data.predicted_temp)}°C` 
    : `${Math.round(data.predicted_temp * 9/5 + 32)}°F`;

  // Determine text color based on theme
  const textColorClass = theme === 'dark' ? 'text-white' : 'text-gray-800';

  return (
    <Card className="w-full max-w-md mx-auto shadow-xl bg-white/30 dark:bg-black/30 backdrop-blur-md">
      <CardHeader className="text-center">
        <CardTitle className={`text-xl font-semibold ${textColorClass}`}>
          Tomorrow's Temperature Forecast
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col items-center space-y-3">
          <div className={`text-5xl font-bold ${textColorClass}`}>
            {temperature}
          </div>
          {data.confidence && (
            <div className={`text-sm ${textColorClass} text-opacity-90`}> {/* Added opacity for subtle difference */}
              Confidence: {data.confidence}%
            </div>
          )}
<footer className="mt-4 text-[0.7rem] text-center text-muted-foreground">
  Disclaimer: This is a machine learning-based prediction and should be treated as an estimate. Actual results may vary.
</footer>
        </div>
      </CardContent>
    </Card>
  );
};

export default PredictionCard;