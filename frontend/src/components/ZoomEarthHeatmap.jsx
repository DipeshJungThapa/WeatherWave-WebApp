import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Thermometer, 
  CloudRain, 
  Wind, 
  Eye, 
  Zap, 
  Mountain, 
  MapPin,
  Maximize2,
  Minimize2,
  RefreshCw,
  Info
} from 'lucide-react';

const NepalWeatherHeatmap = () => {
  const [activeLayer, setActiveLayer] = useState('temperature');
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [currentLocation, setCurrentLocation] = useState({
    lat: 28.3949,
    lon: 84.1240,
    zoom: 7,
    name: 'Nepal Overview'
  });

  // Nepal-specific coordinates and zoom for better focus
  const nepalCoords = {
    lat: 28.3949,
    lon: 84.1240,
    zoom: 7
  };

  // Weather layer configurations
  const weatherLayers = [
    {
      id: 'temperature',
      name: 'Temperature',
      icon: Thermometer,
      color: 'text-red-500',
      bgColor: 'bg-red-50',
      description: 'Real-time temperature across Nepal',
      overlay: 'temp'
    },
    {
      id: 'precipitation',
      name: 'Rainfall',
      icon: CloudRain,
      color: 'text-blue-500',
      bgColor: 'bg-blue-50',
      description: 'Precipitation and rainfall patterns',
      overlay: 'rain'
    },
    {
      id: 'wind',
      name: 'Wind Speed',
      icon: Wind,
      color: 'text-green-500',
      bgColor: 'bg-green-50',
      description: 'Wind speed and direction',
      overlay: 'wind'
    },
    {
      id: 'clouds',
      name: 'Cloud Cover',
      icon: Eye,
      color: 'text-gray-500',
      bgColor: 'bg-gray-50',
      description: 'Cloud coverage and visibility',
      overlay: 'clouds'
    },
    {
      id: 'lightning',
      name: 'Lightning',
      icon: Zap,
      color: 'text-yellow-500',
      bgColor: 'bg-yellow-50',
      description: 'Lightning activity and thunderstorms',
      overlay: 'thunder'
    }
  ];

  // Major Nepal regions for quick navigation
  const nepalRegions = [
    { name: 'Nepal Overview', lat: 28.3949, lon: 84.1240, zoom: 7 },
    { name: 'Kathmandu Valley', lat: 27.7172, lon: 85.3240, zoom: 9 },
    { name: 'Pokhara', lat: 28.2096, lon: 83.9856, zoom: 9 },
    { name: 'Chitwan', lat: 27.5291, lon: 84.3542, zoom: 9 },
    { name: 'Everest Region', lat: 27.9881, lon: 86.9250, zoom: 8 },
    { name: 'Terai Plains', lat: 26.8467, lon: 87.2718, zoom: 7 }
  ];

  const currentLayer = weatherLayers.find(layer => layer.id === activeLayer);

  const getWindyUrl = (overlay, lat = currentLocation.lat, lon = currentLocation.lon, zoom = currentLocation.zoom) => {
    return `https://embed.windy.com/embed2.html?lat=${lat}&lon=${lon}&detailLat=${lat}&detailLon=${lon}&width=100%&height=100%&zoom=${zoom}&level=surface&overlay=${overlay}&menu=&message=true&marker=&calendar=now&pressure=true&type=map&location=coordinates&detail=true&metricWind=default&metricTemp=default&radarRange=-1`;
  };

  const handleLocationChange = (region) => {
    setIsLoading(true);
    setCurrentLocation({
      lat: region.lat,
      lon: region.lon,
      zoom: region.zoom,
      name: region.name
    });
    // Simulate loading time for the iframe to update
    setTimeout(() => setIsLoading(false), 1500);
  };

  const handleRefresh = () => {
    setIsLoading(true);
    setLastUpdated(new Date());
    // Simulate refresh
    setTimeout(() => setIsLoading(false), 1000);
  };

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  useEffect(() => {
    const timer = setTimeout(() => setIsLoading(false), 2000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <Card className={`mt-8 transition-all duration-300 ${isFullscreen ? 'fixed inset-4 z-50 bg-white' : 'bg-white/30 dark:bg-black/30 backdrop-blur-md'}`}>
      <CardHeader className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Mountain className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <CardTitle className="text-2xl text-foreground">
                Nepal Weather Live Map
              </CardTitle>
              <p className="text-sm text-muted-foreground mt-1">
                {currentLocation.name} • Updated {lastUpdated.toLocaleTimeString()}
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={handleRefresh}
              disabled={isLoading}
              className="text-muted-foreground hover:text-foreground"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleFullscreen}
              className="text-muted-foreground hover:text-foreground"
            >
              {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
            </Button>
          </div>
        </div>

        {/* Weather Layer Tabs */}
        <Tabs value={activeLayer} onValueChange={setActiveLayer} className="w-full">
          <TabsList className="grid w-full grid-cols-5 bg-gray-100 dark:bg-gray-800">
            {weatherLayers.map((layer) => {
              const IconComponent = layer.icon;
              return (
                <TabsTrigger
                  key={layer.id}
                  value={layer.id}
                  className="flex items-center gap-2 data-[state=active]:bg-white data-[state=active]:shadow-sm"
                >
                  <IconComponent className={`w-4 h-4 ${layer.color}`} />
                  <span className="hidden sm:inline">{layer.name}</span>
                </TabsTrigger>
              );
            })}
          </TabsList>

          {/* Active Layer Info */}
          <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
            <div className="flex items-center gap-3">
              <div className={`p-2 ${currentLayer?.bgColor} rounded-lg`}>
                <currentLayer.icon className={`w-5 h-5 ${currentLayer?.color}`} />
              </div>
              <div>
                <h4 className="font-medium text-foreground">{currentLayer?.name} Map</h4>
                <p className="text-sm text-muted-foreground">{currentLayer?.description}</p>
              </div>
            </div>
            <Badge variant="secondary" className="gap-1">
              <Info className="w-3 h-3" />
              Live Data
            </Badge>
          </div>
        </Tabs>

        {/* Quick Region Navigation */}
        <div className="space-y-2">
          <h4 className="text-sm font-medium text-muted-foreground flex items-center gap-2">
            <MapPin className="w-4 h-4" />
            Quick Navigation
          </h4>
          <div className="flex flex-wrap gap-2">
            {nepalRegions.map((region) => (
              <Button
                key={region.name}
                variant={currentLocation.name === region.name ? "default" : "outline"}
                size="sm"
                className="text-xs transition-all duration-200 hover:scale-105"
                onClick={() => handleLocationChange(region)}
                disabled={isLoading}
              >
                {region.name}
              </Button>
            ))}
          </div>
        </div>
      </CardHeader>

      <CardContent>
        <div className={`relative overflow-hidden rounded-xl shadow-lg ${isFullscreen ? 'h-[calc(100vh-300px)]' : 'h-[500px] lg:h-[600px]'}`}>
          {isLoading && (
            <div className="absolute inset-0 bg-gray-100 dark:bg-gray-800 flex items-center justify-center z-10">
              <div className="text-center space-y-3">
                <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
                <p className="text-sm text-muted-foreground">Loading weather data...</p>
              </div>
            </div>
          )}
          
          <iframe
            key={`${currentLocation.lat}-${currentLocation.lon}-${activeLayer}`}
            title={`Nepal Weather Map - ${currentLayer?.name} - ${currentLocation.name}`}
            width="100%"
            height="100%"
            src={getWindyUrl(currentLayer?.overlay)}
            frameBorder="0"
            className="w-full h-full transition-opacity duration-300"
            style={{ opacity: isLoading ? 0.3 : 1 }}
            onLoad={() => setIsLoading(false)}
          />
          
          {/* Map Controls Overlay */}
          <div className="absolute bottom-4 left-4 bg-white/90 dark:bg-black/90 backdrop-blur-sm rounded-lg p-3 shadow-lg">
            <div className="text-xs text-muted-foreground space-y-1">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span>Live Data</span>
              </div>
              <div className="flex items-center gap-2">
                <Mountain className="w-3 h-3" />
                <span>Nepal Focus</span>
              </div>
            </div>
          </div>

          {/* Legend for current layer */}
          <div className="absolute top-4 right-4 bg-white/90 dark:bg-black/90 backdrop-blur-sm rounded-lg p-3 shadow-lg max-w-xs">
            <div className="text-xs space-y-2">
              <div className="flex items-center gap-2 font-medium">
                <currentLayer.icon className={`w-4 h-4 ${currentLayer?.color}`} />
                <span>{currentLayer?.name} Legend</span>
              </div>
              <div className="text-muted-foreground">
                {activeLayer === 'temperature' && 'Red: Hot • Blue: Cold'}
                {activeLayer === 'precipitation' && 'Blue: Heavy Rain • Green: Light Rain'}
                {activeLayer === 'wind' && 'Green: Light • Yellow: Strong • Red: Very Strong'}
                {activeLayer === 'clouds' && 'White: Clear • Gray: Cloudy'}
                {activeLayer === 'lightning' && 'Yellow: Lightning Activity • Red: Severe'}
              </div>
            </div>
          </div>
        </div>

        {/* Additional Info */}
        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div className="flex items-center gap-2 text-muted-foreground">
            <RefreshCw className="w-4 h-4" />
            <span>Updates every 15 minutes</span>
          </div>
          <div className="flex items-center gap-2 text-muted-foreground">
            <Mountain className="w-4 h-4" />
            <span>Optimized for Nepal geography</span>
          </div>
          <div className="flex items-center gap-2 text-muted-foreground">
            <Eye className="w-4 h-4" />
            <span>High-resolution satellite data</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default NepalWeatherHeatmap;
