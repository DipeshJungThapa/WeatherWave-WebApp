import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { 
  Cloud, 
  Sun, 
  CloudRain, 
  Wind, 
  AlertTriangle,
  ExternalLink,
  RefreshCw,
  Globe,
  MapPin
} from 'lucide-react';

const WeatherNews = () => {
  const [newsItems, setNewsItems] = useState([]);
  const [currentMethod, setCurrentMethod] = useState('curated');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Local fallback Nepal Weather News (if backend fails)
  const getCuratedNepalWeatherNews = () => {
    const currentSeason = getCurrentSeason();
    const weatherContext = getSeasonalWeatherContext(currentSeason);
    
    return [
      {
        id: 1,
        title: `${currentSeason} Weather Update: ${weatherContext.mainCondition}`,
        description: `Current weather patterns show ${weatherContext.description}. ${weatherContext.advisory}`,
        source: "Nepal Weather Monitor",
        timestamp: new Date().toLocaleDateString(),
        severity: weatherContext.severity,
        location: "Kathmandu Valley",
        type: "forecast",
        link: "https://www.dhm.gov.np/"
      },
      {
        id: 2,
        title: "Weather Safety Advisory for Nepal",
        description: "Department of Hydrology and Meteorology provides general weather advisories for all regions of Nepal.",
        source: "DHM Nepal",
        timestamp: new Date().toLocaleDateString(),
        severity: "moderate",
        location: "Nepal",
        type: "advisory",
        link: "https://www.dhm.gov.np/"
      }
    ];
  };

  // Utility Functions
  const getCurrentSeason = () => {
    const month = new Date().getMonth();
    if (month >= 2 && month <= 5) return "Spring";
    if (month >= 6 && month <= 8) return "Monsoon"; 
    if (month >= 9 && month <= 11) return "Autumn";
    return "Winter";
  };

  const getSeasonalWeatherContext = (season) => {
    const contexts = {
      "Monsoon": {
        mainCondition: "Heavy Rainfall Expected",
        description: "active monsoon patterns with frequent precipitation",
        advisory: "Avoid travel in flood-prone areas and carry umbrellas.",
        severity: "moderate",
        tempRange: "24-30°C"
      },
      "Winter": {
        mainCondition: "Clear Skies Prevail", 
        description: "dry and cold conditions with minimal precipitation",
        advisory: "Dress warmly, especially during morning and evening hours.",
        severity: "low",
        tempRange: "8-22°C"
      },
      "Spring": {
        mainCondition: "Pleasant Weather Returns",
        description: "warming temperatures with occasional light showers", 
        advisory: "Ideal conditions for outdoor activities and travel.",
        severity: "low",
        tempRange: "15-28°C"
      },
      "Autumn": {
        mainCondition: "Post-Monsoon Clarity",
        description: "clear skies with reduced humidity and stable weather",
        advisory: "Excellent visibility for mountain viewing and trekking.",
        severity: "low", 
        tempRange: "12-26°C"
      }
    };
    
    return contexts[season] || contexts["Winter"];
  };

  // Main news fetching function
  const fetchAllWeatherNews = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Call the backend curated news endpoint
      const response = await fetch('http://localhost:8000/api/weather-news/');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data && data.length > 0) {
        setNewsItems(data);
        setCurrentMethod('curated');
      } else {
        // Fallback to local content if backend returns empty
        setNewsItems(getCuratedNepalWeatherNews());
        setCurrentMethod('local');
      }
      
    } catch (error) {
      console.error('Error fetching weather news from backend:', error);
      setError('Unable to load latest news. Showing local content.');
      
      // Fallback to local news on error
      setNewsItems(getCuratedNepalWeatherNews());
      setCurrentMethod('local');
    } finally {
      setLoading(false);
    }
  };

  // Load news on component mount
  useEffect(() => {
    fetchAllWeatherNews();
  }, []);

  // Get severity color
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high': return 'text-red-600 bg-red-50 border-red-200';
      case 'moderate': return 'text-yellow-600 bg-yellow-50 border-yellow-200';  
      case 'low': return 'text-green-600 bg-green-50 border-green-200';
      default: return 'text-blue-600 bg-blue-50 border-blue-200';
    }
  };

  // Get weather icon
  const getWeatherIcon = (type) => {
    switch (type) {
      case 'alert': return <AlertTriangle className="h-4 w-4" />;
      case 'forecast': return <Cloud className="h-4 w-4" />;
      case 'advisory': return <Wind className="h-4 w-4" />;
      case 'analysis': return <Sun className="h-4 w-4" />;
      case 'traditional': return <Globe className="h-4 w-4" />;
      default: return <CloudRain className="h-4 w-4" />;
    }
  };

  return (
    <Card className="w-full bg-white/30 dark:bg-black/30 backdrop-blur-md">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-bold flex items-center gap-2">
            <CloudRain className="h-5 w-5" />
            Nepal Weather News
          </CardTitle>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={fetchAllWeatherNews}
            disabled={loading}
            className="p-2 rounded-full bg-blue-100 hover:bg-blue-200 dark:bg-blue-900 dark:hover:bg-blue-800 transition-colors"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          </motion.button>
        </div>
        <p className="text-sm text-muted-foreground">
          Latest weather news and updates for Nepal
        </p>
      </CardHeader>

      <CardContent className="space-y-3 max-h-80 overflow-y-auto">
        {error && (
          <div className="text-sm text-amber-600 bg-amber-50 p-2 rounded border border-amber-200">
            {error}
          </div>
        )}

        <AnimatePresence>
          {newsItems.map((item, index) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className={`p-3 rounded-lg border ${getSeverityColor(item.severity)} transition-all hover:shadow-sm`}
            >
              <div className="flex items-start gap-3">
                <div className="mt-1">
                  {getWeatherIcon(item.type)}
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2">
                    <h3 className="font-medium text-sm leading-tight">
                      {item.title}
                    </h3>
                    {item.link && (
                      <a
                        href={item.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 flex-shrink-0"
                      >
                        <ExternalLink className="h-3 w-3" />
                      </a>
                    )}
                  </div>
                  
                  <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                    {item.description}
                  </p>
                  
                  <div className="flex items-center justify-between mt-2 text-xs text-muted-foreground">
                    <div className="flex items-center gap-3">
                      <span>{item.source}</span>
                      <span className="flex items-center gap-1">
                        <MapPin className="h-3 w-3" />
                        {item.location}
                      </span>
                    </div>
                    <span>{item.timestamp}</span>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {newsItems.length === 0 && !loading && (
          <div className="text-center py-4 text-muted-foreground">
            <Cloud className="h-8 w-8 mx-auto mb-2" />
            <p className="text-sm">No weather news available at the moment.</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default WeatherNews;
