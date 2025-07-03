import React from 'react';
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardFooter
} from './ui/card';
import { AirVent } from 'lucide-react';

const getAqiInfo = (value) => {
  if (value <= 50) return { label: "Good", color: "text-green-500", ring: "ring-green-500" };
  if (value <= 100) return { label: "Moderate", color: "text-yellow-500", ring: "ring-yellow-500" };
  if (value <= 150) return { label: "Unhealthy for Sensitive", color: "text-orange-500", ring: "ring-orange-500" };
  if (value <= 200) return { label: "Unhealthy", color: "text-red-500", ring: "ring-red-500" };
  if (value <= 300) return { label: "Very Unhealthy", color: "text-purple-500", ring: "ring-purple-500" };
  return { label: "Hazardous", color: "text-red-800", ring: "ring-red-800" };
};

export default function AQICard({ data }) {
  const value = data?.AQI_Value;
  const info = value != null ? getAqiInfo(value) : null;

  return (
    <Card className="hover:shadow-lg transition-shadow flex flex-col justify-between">
      <CardHeader>
        <CardTitle className="text-lg">Air Quality</CardTitle>
      </CardHeader>

      <CardContent className="flex-1 flex flex-col items-center justify-center space-y-2">
        {!info ? (
          <p className="text-center text-sm text-muted-foreground">No AQI data available</p>
        ) : (
          <>
            <div
              className={`p-4 rounded-full bg-popover ring-4 ${info.ring} flex items-center justify-center`}
            >
              <AirVent className={`h-8 w-8 ${info.color}`} />
            </div>
            <div className="text-4xl font-extrabold">
              <span className={info.color}>{value}</span>
            </div>
            <p className={`text-sm font-medium ${info.color}`}>{info.label}</p>
          </>
        )}
      </CardContent>

      <CardFooter className="text-xs text-muted-foreground text-center">
        PM2.5 based AQI
      </CardFooter>
    </Card>
  );
}
