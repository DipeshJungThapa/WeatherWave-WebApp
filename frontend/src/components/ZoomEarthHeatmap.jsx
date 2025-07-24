import React from 'react';

const ZoomEarthHeatmap = () => {
  return (
    <div className="mt-8 bg-white/30 dark:bg-black/30 backdrop-blur-md p-6 rounded-2xl shadow-lg space-y-4">
  <h2 className="text-2xl font-semibold text-foreground">
    🌡️🌧️ Live Heatmap (Nepal: Temperature, Rain & More)
  </h2>
      <div className="w-full h-[700px] overflow-hidden rounded-2xl shadow-lg">
        <iframe
          title="Windy Heatmap"
          width="100%"
          height="100%"
          src="https://embed.windy.com/embed2.html?lat=28.4&lon=84.1&detailLat=28.4&detailLon=84.1&width=100%&height=100%&zoom=7&level=surface&overlay=temperature&menu=&message=true&marker=&calendar=now&pressure=true&type=map&location=coordinates&detail=true&metricWind=default&metricTemp=default&radarRange=-1"
          frameBorder="0"
          className="w-full h-full"
        ></iframe>
      </div>
    </div>
  );
};

export default ZoomEarthHeatmap;
