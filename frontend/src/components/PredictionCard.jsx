// src/components/PredictionCard.jsx
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card'; // Adjust path to shadcn/ui Card
import { Alert, AlertDescription, AlertTitle } from './ui/alert'; // Adjust path to shadcn/ui Alert
import { Badge } from './ui/badge'; // Adjust path to shadcn/ui Badge

const PredictionCard = ({ data }) => {
  if (!data) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>ML Prediction</CardTitle>
        </CardHeader>
        <CardContent>
          <p>No prediction data available.</p>
        </CardContent>
      </Card>
    );
  }

  // You will populate this with actual prediction data later in Step 4
  return (
    <Card>
      <CardHeader>
        <CardTitle>Tomorrow's Prediction</CardTitle>
        <CardDescription>Based on Machine Learning</CardDescription>
      </CardHeader>
      <CardContent>
        {data.predicted_temp ? (
          <Alert>
            <AlertTitle>Predicted Temperature</AlertTitle>
            <AlertDescription>
              Tomorrow: <Badge>{data.predicted_temp}°C</Badge>
              {data.confidence && ` (Confidence: ${data.confidence}%)`}
            </AlertDescription>
          </Alert>
        ) : (
          <p>Prediction not available.</p>
        )}
        <p className="mt-2">This is a placeholder for PredictionCard content.</p>
      </CardContent>
    </Card>
  );
};

export default PredictionCard;