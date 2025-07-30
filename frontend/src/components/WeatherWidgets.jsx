import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { ExternalLink, Maximize2, Minimize2 } from 'lucide-react';

const WeatherWidgets = () => {
  const [expandedWidget, setExpandedWidget] = useState(null);
  const [showIframes, setShowIframes] = useState(false);

  // Enable iframes after component mount (better performance)
  useEffect(() => {
    const timer = setTimeout(() => setShowIframes(true), 1000);
    return () => clearTimeout(timer);
  }, []);

  const widgets = [
    {
      id: 'meteoblue',
      title: 'MeteoBlue Nepal Forecast',
      description: 'Professional weather forecasts for Nepal',
      url: 'https://www.meteoblue.com/en/weather/widget/daily/kathmandu_nepal_1283240?geoloc=fixed&days=7&tempunit=CELSIUS&windunit=KILOMETER_PER_HOUR&precipunit=MILLIMETER&coloured=coloured&pictoicon=0&pictoicon=1&maxtemperature=0&maxtemperature=1&mintemperature=0&mintemperature=1&windspeed=0&windspeed=1&windgust=0&winddirection=0&winddirection=1&uv=0&humidity=0&precipitation=0&precipitation=1&precipitationprobability=0&precipitationprobability=1&spot=0&pressure=0&layout=light',
      width: '100%',
      height: '400px',
      type: 'embedded'
    },
    {
      id: 'windy',
      title: 'Windy Weather Map - Nepal',
      description: 'Interactive weather visualization',
      url: 'https://embed.windy.com/embed2.html?lat=28.394&lon=84.124&detailLat=27.717&detailLon=85.324&width=650&height=450&zoom=6&level=surface&overlay=wind&product=ecmwf&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1',
      width: '100%', 
      height: '450px',
      type: 'embedded'
    },
    {
      id: 'hamropatro',
      title: 'Hamro Patro Weather',
      description: 'Traditional Nepali weather information',
      url: 'https://www.hamropatro.com/weather',
      width: '100%',
      height: '350px',
      type: 'link' // This will be a link instead of iframe
    }
  ];

  const NewsLinks = () => (
    <div className="space-y-3">
      <h3 className="font-semibold text-sm">Direct Weather News Sources</h3>
      
      <div className="grid gap-2">
        <a
          href="https://kathmandupost.com/weather"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center justify-between p-3 bg-blue-50 dark:bg-blue-900/30 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/50 transition-colors group"
        >
          <div>
            <div className="font-medium text-sm">The Kathmandu Post - Weather</div>
            <div className="text-xs text-muted-foreground">Daily weather reports and forecasts</div>
          </div>
          <ExternalLink className="h-4 w-4 opacity-50 group-hover:opacity-100" />
        </a>

        <a
          href="https://myrepublica.nagariknetwork.com/news/heavy-rainfall-likely-in-isolated-places-in-gandaki-79-46.html"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center justify-between p-3 bg-green-50 dark:bg-green-900/30 rounded-lg hover:bg-green-100 dark:hover:bg-green-900/50 transition-colors group"
        >
          <div>
            <div className="font-medium text-sm">My Republica - Weather News</div>
            <div className="text-xs text-muted-foreground">Latest weather updates and alerts</div>
          </div>
          <ExternalLink className="h-4 w-4 opacity-50 group-hover:opacity-100" />
        </a>

        <a
          href="https://www.meteoblue.com/en/weather/week/kathmandu_nepal_1283240"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center justify-between p-3 bg-purple-50 dark:bg-purple-900/30 rounded-lg hover:bg-purple-100 dark:hover:bg-purple-900/50 transition-colors group"
        >
          <div>
            <div className="font-medium text-sm">MeteoBlue Nepal</div>
            <div className="text-xs text-muted-foreground">Professional meteorological forecasts</div>
          </div>
          <ExternalLink className="h-4 w-4 opacity-50 group-hover:opacity-100" />
        </a>

        <a
          href="https://windy.com/?28.394,84.124,6"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center justify-between p-3 bg-orange-50 dark:bg-orange-900/30 rounded-lg hover:bg-orange-100 dark:hover:bg-orange-900/50 transition-colors group"
        >
          <div>
            <div className="font-medium text-sm">Windy - Nepal Weather</div>
            <div className="text-xs text-muted-foreground">Interactive weather maps and radar</div>
          </div>
          <ExternalLink className="h-4 w-4 opacity-50 group-hover:opacity-100" />
        </a>
      </div>
    </div>
  );

  const toggleWidget = (widgetId) => {
    setExpandedWidget(expandedWidget === widgetId ? null : widgetId);
  };

  return (
    <div className="space-y-4">
      {/* Quick Links Section */}
      <Card className="w-full bg-white/30 dark:bg-black/30 backdrop-blur-md">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg font-bold">Quick Weather Sources</CardTitle>
          <p className="text-sm text-muted-foreground">
            Direct links to reliable Nepal weather information
          </p>
        </CardHeader>
        <CardContent>
          <NewsLinks />
        </CardContent>
      </Card>

      {/* Embeddable Widgets Section */}
      <Card className="w-full bg-white/30 dark:bg-black/30 backdrop-blur-md">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg font-bold">Weather Widgets</CardTitle>
          <p className="text-sm text-muted-foreground">
            Interactive weather forecasts (click to expand)
          </p>
        </CardHeader>
        <CardContent className="space-y-4">
          {widgets.map((widget) => (
            <div key={widget.id} className="border rounded-lg overflow-hidden">
              <div 
                className="flex items-center justify-between p-3 bg-muted/50 cursor-pointer hover:bg-muted transition-colors"
                onClick={() => toggleWidget(widget.id)}
              >
                <div>
                  <h3 className="font-medium text-sm">{widget.title}</h3>
                  <p className="text-xs text-muted-foreground">{widget.description}</p>
                </div>
                {expandedWidget === widget.id ? (
                  <Minimize2 className="h-4 w-4" />
                ) : (
                  <Maximize2 className="h-4 w-4" />
                )}
              </div>

              {expandedWidget === widget.id && (
                <div className="p-3 bg-white dark:bg-gray-900">
                  {widget.type === 'embedded' && showIframes ? (
                    <div className="w-full overflow-hidden rounded">
                      <iframe
                        src={widget.url}
                        width={widget.width}
                        height={widget.height}
                        frameBorder="0"
                        scrolling="no"
                        allowTransparency="true"
                        sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
                        title={widget.title}
                        className="w-full border-0 rounded"
                      />
                    </div>
                  ) : widget.type === 'link' ? (
                    <div className="text-center py-8">
                      <p className="mb-4 text-sm text-muted-foreground">
                        Click below to visit {widget.title}
                      </p>
                      <a
                        href={widget.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                      >
                        Open {widget.title}
                        <ExternalLink className="h-4 w-4" />
                      </a>
                    </div>
                  ) : (
                    <div className="text-center py-4 text-muted-foreground">
                      <p className="text-sm">Loading widget...</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Implementation Guide */}
      <Card className="w-full bg-white/30 dark:bg-black/30 backdrop-blur-md">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg font-bold">Implementation Guide</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="text-sm space-y-2">
            <h4 className="font-medium">🎯 Free Solutions (No API Keys):</h4>
            <ul className="list-disc list-inside space-y-1 text-muted-foreground ml-2">
              <li><strong>Direct Links:</strong> Link to Kathmandu Post, My Republica weather sections</li>
              <li><strong>MeteoBlue Widget:</strong> Free embeddable weather forecasts</li>
              <li><strong>Windy Embed:</strong> Interactive weather maps</li>
              <li><strong>RSS Alternative:</strong> Curated news system (already implemented)</li>
            </ul>
            
            <h4 className="font-medium mt-4">🔧 Easy Integration:</h4>
            <ul className="list-disc list-inside space-y-1 text-muted-foreground ml-2">
              <li>Copy any widget iframe code for your own site</li>
              <li>Use the news links as quick reference buttons</li>
              <li>Implement RSS parsing with rss-parser library</li>
              <li>All solutions work without backend processing</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default WeatherWidgets;
