import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Skeleton } from './ui/skeleton';
import { 
  ExternalLink, 
  Clock, 
  Newspaper, 
  RefreshCw,
  Globe,
  AlertTriangle,
  CloudRain,
  Sun,
  Mountain,
  Thermometer,
  Wind
} from 'lucide-react';

const WeatherNews = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  // Real Nepal news sources RSS feeds with additional sources
  const NEWS_SOURCES = [
    {
      name: "Kantipur Daily",
      rssUrl: "https://ekantipur.com/rss",
      domain: "ekantipur.com"
    },
    {
      name: "Himalayan Times",
      rssUrl: "https://thehimalayantimes.com/rss",
      domain: "thehimalayantimes.com"
    },
    {
      name: "Online Khabar",
      rssUrl: "https://www.onlinekhabar.com/rss",
      domain: "onlinekhabar.com"
    },
    {
      name: "Republica",
      rssUrl: "https://myrepublica.nagariknetwork.com/rss",
      domain: "myrepublica.nagariknetwork.com"
    },
    {
      name: "Setopati",
      rssUrl: "https://setopati.com/rss",
      domain: "setopati.com"
    },
    {
      name: "Ratopati",
      rssUrl: "https://ratopati.com/rss.xml",
      domain: "ratopati.com"
    },
    {
      name: "Annapurna Post", 
      rssUrl: "https://annapurnapost.com/rss",
      domain: "annapurnapost.com"
    }
  ];

  // Enhanced weather-related keywords for filtering
  const WEATHER_KEYWORDS = [
    // English weather terms
    'weather', 'rain', 'monsoon', 'flood', 'drought', 'temperature', 'climate',
    'storm', 'wind', 'snow', 'heat', 'cold', 'lightning', 'thunder',
    'precipitation', 'humidity', 'cyclone', 'tornado', 'hail', 'fog',
    'forecast', 'meteorology', 'seasonal', 'rainfall', 'snowfall',
    'landslide', 'avalanche', 'tsunami', 'earthquake', 'heatwave',
    
    // Nepali weather terms  
    'मनसुन', 'वर्षा', 'बाढी', 'खडेरी', 'तापक्रम', 'मौसम', 'हावाहुरी',
    'हिमपात', 'चट्याङ', 'बादल', 'तुषारपात', 'गर्मी', 'चिसो',
    'मौसमी', 'पानी', 'आँधी', 'बर्फ', 'घाम', 'छाया',
    
    // Weather-related events in Nepal
    'जाडो', 'गर्मी', 'शीत', 'ग्रीष्म', 'शरद', 'बसन्त'
  ];

  const NEPAL_LOCATION_KEYWORDS = [
    // Major cities and regions
    'nepal', 'kathmandu', 'pokhara', 'chitwan', 'everest', 'himalaya',
    'terai', 'madhesh', 'bagmati', 'gandaki', 'karnali', 'sudurpaschim',
    'lalitpur', 'bhaktapur', 'biratnagar', 'birgunj', 'dharan', 'butwal',
    'nepalgunj', 'janakpur', 'hetauda', 'dhangadhi', 'mahendranagar',
    
    // Nepali location terms
    'नेपाल', 'काठमाडौं', 'पोखरा', 'चितवन', 'हिमालय', 'तराई',
    'लालितपुर', 'भक्तपुर', 'विराटनगर', 'वीरगञ्ज', 'धरान',
    'बुटवल', 'नेपालगञ्ज', 'जनकपुर', 'हेटौडा',
    
    // Geographical features
    'mount everest', 'annapurna', 'manaslu', 'makalu', 'cho oyu',
    'sagarmatha', 'mahakali', 'karnali river', 'narayani', 'koshi'
  ];

  const fetchRealNews = async (isRefresh = false) => {
    try {
      setRefreshing(true);
      const allNews = [];

      // Enhanced RSS sources with backup endpoints
      const enhancedSources = NEWS_SOURCES.map(source => ({
        ...source,
        // Add backup RSS endpoints for some sources
        backupUrls: source.name === 'Online Khabar' ? [
          'https://www.onlinekhabar.com/feed',
          'https://www.onlinekhabar.com/category/news/feed'
        ] : source.name === 'Kantipur Daily' ? [
          'https://ekantipur.com/feed',
          'https://ekantipur.com/rss.xml'
        ] : []
      }));

      for (const source of enhancedSources) {
        let sourceSuccess = false;
        const urlsToTry = [source.rssUrl, ...source.backupUrls];

        for (const rssUrl of urlsToTry) {
          if (sourceSuccess) break;

          try {
            console.log(`Trying RSS feed: ${rssUrl} for ${source.name}`);
            
            // Try RSS2JSON API first with longer timeout
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 15000); // 15 second timeout

            let response = await fetch(
              `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(rssUrl)}&count=15`,
              {
                headers: {
                  'Accept': 'application/json',
                },
                signal: controller.signal
              }
            );

            clearTimeout(timeoutId);

            if (response.ok) {
              const data = await response.json();
              
              if (data.status === 'ok' && data.items && data.items.length > 0) {
                console.log(`✅ Successfully fetched ${data.items.length} items from ${source.name} via RSS2JSON`);
                
                // Filter for weather and Nepal-related content with enhanced keywords
                const weatherNews = data.items.filter(item => {
                  const title = (item.title || '').toLowerCase();
                  const description = (item.description || '').toLowerCase();
                  const content = title + ' ' + description;
                  
                  // More flexible matching
                  const hasWeatherKeyword = WEATHER_KEYWORDS.some(keyword => 
                    content.includes(keyword.toLowerCase())
                  );
                  
                  // Also include general news that might be weather-related
                  const hasWeatherContext = [
                    'weather', 'climate', 'temperature', 'rain', 'storm', 'flood', 'drought',
                    'मौसम', 'वर्षा', 'बाढी'
                  ].some(keyword => content.includes(keyword.toLowerCase()));
                  
                  const hasNepalLocation = NEPAL_LOCATION_KEYWORDS.some(keyword => 
                    content.includes(keyword.toLowerCase())
                  );
                  
                  return (hasWeatherKeyword || hasWeatherContext) && hasNepalLocation;
                });

                console.log(`📰 Filtered to ${weatherNews.length} weather-related items from ${source.name}`);

                if (weatherNews.length > 0) {
                  // Transform to our format
                  const transformedNews = weatherNews.slice(0, 5).map((item, index) => {
                    let articleLink = item.link || item.guid || '';
                    
                    if (articleLink && !articleLink.startsWith('http')) {
                      const baseUrl = `https://${source.domain}`;
                      articleLink = articleLink.startsWith('/') 
                        ? `${baseUrl}${articleLink}` 
                        : `${baseUrl}/${articleLink}`;
                    }
                    
                    if (!articleLink || articleLink.includes('localhost')) {
                      articleLink = `https://${source.domain}`;
                    }

                    return {
                      id: `${source.domain}-${Date.now()}-${index}`,
                      title: item.title || 'Weather News Update',
                      titleEn: item.title || 'Weather News Update',
                      description: item.description?.replace(/<[^>]*>/g, '')?.substring(0, 200) || 'Weather update from Nepal.',
                      link: articleLink,
                      pubDate: item.pubDate || new Date().toISOString(),
                      source: source.name,
                      category: getWeatherCategory(item.title + ' ' + item.description),
                      weatherType: getWeatherType(item.title + ' ' + item.description),
                      thumbnail: item.thumbnail || item.enclosure?.link || 'https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?w=400&h=200&fit=crop',
                      priority: 1
                    };
                  });

                  allNews.push(...transformedNews);
                  sourceSuccess = true;
                }
              }
            }

            // If RSS2JSON fails, try alternative method
            if (!sourceSuccess) {
              console.log(`⚠️ RSS2JSON failed for ${source.name}, trying alternative method...`);
              
              try {
                const altResponse = await fetch(
                  `https://api.allorigins.win/get?url=${encodeURIComponent(rssUrl)}`,
                  {
                    headers: { 'Accept': 'application/json' },
                    signal: AbortSignal.timeout(10000) // 10 second timeout
                  }
                );
                
                if (altResponse.ok) {
                  const altData = await altResponse.json();
                  console.log(`📡 Alternative fetch successful for ${source.name}`, altData.status);
                  // We could parse XML here but for now just log success
                }
              } catch (altError) {
                console.log(`❌ Alternative method also failed for ${source.name}:`, altError.message);
              }
            }

          } catch (sourceError) {
            console.warn(`❌ Failed to fetch from ${source.name} with URL ${rssUrl}:`, sourceError.message);
          }
        }

        if (!sourceSuccess) {
          console.log(`⚠️ All attempts failed for ${source.name}`);
        }
      }

      // Handle the results
      if (allNews.length > 0) {
        // Sort by date and take the most recent
        allNews.sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate));
        const latestNews = allNews.slice(0, 12); // Increased to 12 items
        setNews(latestNews);
        setError(null);
        console.log(`✅ Successfully updated with ${latestNews.length} total weather news items`);
      } else {
        // Enhanced fallback handling
        if (isRefresh && news.length > 0) {
          setError('No new weather updates found. Showing previous news.');
          console.log('🔄 No new weather news found, keeping existing news');
        } else {
          // Create more realistic fallback content
          const fallbackNews = [
            {
              id: 'fallback-1',
              title: "Nepal Weather Services Temporarily Unavailable",
              titleEn: "Weather news feeds being restored",
              description: "We're working to restore live weather news from major Nepal sources including Kantipur Daily, Himalayan Times, Online Khabar, Republica, and Setopati. Please check back shortly.",
              link: "https://ekantipur.com",
              pubDate: new Date().toISOString(),
              source: "WeatherWave",
              category: "System Info",
              weatherType: "System",
              thumbnail: "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?w=400&h=200&fit=crop",
              priority: 1
            },
            {
              id: 'fallback-2', 
              title: "Check Official Weather Sources",
              titleEn: "Alternative weather information",
              description: "For immediate weather updates, visit official sources like Department of Hydrology and Meteorology or major Nepal news portals directly.",
              link: "https://www.dhm.gov.np",
              pubDate: new Date(Date.now() - 60000).toISOString(),
              source: "WeatherWave",
              category: "Advisory",
              weatherType: "General Weather",
              thumbnail: "https://images.unsplash.com/photo-1592210454359-9043f067919b?w=400&h=200&fit=crop",
              priority: 2
            }
          ];
          
          setNews(fallbackNews);
          setError('Weather news feeds temporarily unavailable. Showing alternative information.');
        }
      }

    } catch (err) {
      console.error('Error fetching real Nepal weather news:', err);
      
      // If refresh fails, keep existing news and show error
      if (isRefresh && news.length > 0) {
        setError('Failed to refresh. Showing previous news.');
      } else {
        setError('Unable to load latest weather updates from news sources');
        // Only show fallback if no existing news
        if (news.length === 0) {
          setNews([
            {
              id: 'demo-real-1',
              title: "Live news from Nepal sources temporarily unavailable",
              titleEn: "Weather news integration in progress", 
              description: "We're working to connect with live RSS feeds from Kantipur, Himalayan Times, Online Khabar, Republica, and Setopati for real-time Nepal weather news.",
              link: "https://ekantipur.com",
              pubDate: new Date().toISOString(),
              source: "System Message",
              category: "System Info", 
              weatherType: "System",
              thumbnail: "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?w=400&h=200&fit=crop",
              priority: 1
            }
          ]);
        }
      }
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const getWeatherCategory = (content) => {
    const lowerContent = content.toLowerCase();
    if (lowerContent.includes('flood') || lowerContent.includes('बाढी')) return 'Flood Alert';
    if (lowerContent.includes('drought') || lowerContent.includes('खडेरी')) return 'Drought Alert';
    if (lowerContent.includes('monsoon') || lowerContent.includes('मनसुन')) return 'Monsoon Update';
    if (lowerContent.includes('storm') || lowerContent.includes('हावाहुरी')) return 'Storm Warning';
    if (lowerContent.includes('heat') || lowerContent.includes('गर्मी')) return 'Heat Alert';
    if (lowerContent.includes('snow') || lowerContent.includes('हिमपात')) return 'Snow Alert';
    return 'Weather News';
  };

  const getWeatherType = (content) => {
    const lowerContent = content.toLowerCase();
    if (lowerContent.includes('rain') || lowerContent.includes('वर्षा')) return 'Heavy Rain';
    if (lowerContent.includes('storm') || lowerContent.includes('हावाहुरी')) return 'Thunderstorm';
    if (lowerContent.includes('heat') || lowerContent.includes('गर्मी')) return 'Heat Wave';
    if (lowerContent.includes('snow') || lowerContent.includes('हिमपात')) return 'Heavy Snow';
    if (lowerContent.includes('drought') || lowerContent.includes('खडेरी')) return 'Drought';
    return 'General Weather';
  };

  const handleRefresh = () => {
    fetchRealNews(true); // Pass true to indicate this is a manual refresh
  };

  useEffect(() => {
    fetchRealNews(false); // Initial load, not a refresh
    
    // Auto-refresh every 30 minutes for real news
    const interval = setInterval(() => {
      fetchRealNews(true); // Auto-refresh, preserve existing news if fails
    }, 30 * 60 * 1000);

    return () => clearInterval(interval);
  }, []);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInMinutes = Math.floor((now - date) / (1000 * 60));
    
    if (diffInMinutes < 60) {
      return `${diffInMinutes} minutes ago`;
    } else if (diffInMinutes < 1440) {
      const hours = Math.floor(diffInMinutes / 60);
      return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    } else {
      const days = Math.floor(diffInMinutes / 1440);
      return `${days} day${days > 1 ? 's' : ''} ago`;
    }
  };

  const getWeatherIcon = (weatherType) => {
    switch (weatherType) {
      case 'Heavy Rain': return <CloudRain className="w-5 h-5 text-blue-500" />;
      case 'Thunderstorm': return <Wind className="w-5 h-5 text-purple-500" />;
      case 'Heat Wave': return <Thermometer className="w-5 h-5 text-red-500" />;
      case 'Heavy Snow': return <Mountain className="w-5 h-5 text-gray-400" />;
      case 'Drought': return <Sun className="w-5 h-5 text-yellow-500" />;
      case 'System': return <Newspaper className="w-5 h-5 text-gray-500" />;
      default: return <CloudRain className="w-5 h-5 text-blue-500" />;
    }
  };

  const NewsCard = ({ item }) => (
    <Card className="hover:shadow-md transition-all duration-300 group border-l-4 border-l-blue-500">
      <CardContent className="p-4">
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0">
            {getWeatherIcon(item.weatherType)}
          </div>
          
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <Badge variant="secondary" className="text-xs bg-blue-50 text-blue-700 font-semibold">
                {item.category}
              </Badge>
              <Badge variant="outline" className="text-xs font-semibold">
                {item.source}
              </Badge>
            </div>
            
            <h3 className="font-bold text-base mb-1 leading-tight text-gray-900 dark:text-gray-100 group-hover:text-blue-600 transition-colors">
              {item.title}
            </h3>
            
            <p className="text-gray-800 dark:text-gray-200 text-xs mb-2 leading-relaxed line-clamp-2 font-medium">
              {item.description}
            </p>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-xs text-gray-600 font-medium">
                <div className="flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  <span>{formatDate(item.pubDate)}</span>
                </div>
              </div>
              
              <Button
                variant="ghost"
                size="sm"
                className="text-blue-600 hover:text-blue-800 p-1"
                onClick={() => {
                  // Validate URL before opening
                  const url = item.link;
                  console.log('Opening URL:', url); // Debug log
                  
                  if (url && !url.includes('localhost') && (url.startsWith('http://') || url.startsWith('https://'))) {
                    window.open(url, '_blank', 'noopener,noreferrer');
                  } else {
                    // Fallback to source homepage
                    const sourceUrls = {
                      'Kantipur Daily': 'https://ekantipur.com',
                      'Himalayan Times': 'https://thehimalayantimes.com',
                      'Online Khabar': 'https://www.onlinekhabar.com',
                      'Republica': 'https://myrepublica.nagariknetwork.com',
                      'Setopati': 'https://setopati.com'
                    };
                    
                    const fallbackUrl = sourceUrls[item.source] || 'https://ekantipur.com';
                    console.log('Using fallback URL:', fallbackUrl);
                    window.open(fallbackUrl, '_blank', 'noopener,noreferrer');
                  }
                }}
              >
                <ExternalLink className="w-3 h-3" />
              </Button>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Card className="mt-6 bg-white/30 dark:bg-black/30 backdrop-blur-md">
        <CardHeader className="flex flex-row items-center justify-between pb-3">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Newspaper className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <CardTitle className="text-xl text-foreground font-bold">
                Nepal Weather News
              </CardTitle>
              <p className="text-xs text-muted-foreground mt-1 font-medium">
                Loading latest weather updates from Nepal news sources...
              </p>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-3 pt-0">
          {[1, 2, 3].map((i) => (
            <div key={i} className="space-y-2">
              <Skeleton className="h-4 w-3/4" />
              <Skeleton className="h-3 w-full" />
              <Skeleton className="h-3 w-2/3" />
            </div>
          ))}
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="mt-6 bg-white/30 dark:bg-black/30 backdrop-blur-md">
      <CardHeader className="flex flex-row items-center justify-between pb-3">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-100 rounded-lg">
            <Newspaper className="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <CardTitle className="text-xl text-foreground font-bold">
              Nepal Weather News
            </CardTitle>
            <p className="text-xs text-muted-foreground mt-1 font-medium">
              Live updates from major Nepal news sources • Auto-refreshes every 30 min
            </p>
          </div>
        </div>
        
        <Button
          variant="ghost"
          size="sm"
          onClick={handleRefresh}
          disabled={refreshing}
          className="text-muted-foreground hover:text-foreground"
        >
          <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
        </Button>
      </CardHeader>
      
      <CardContent className="pt-0">
        {error && (
          <div className="mb-4 p-3 bg-orange-50 border border-orange-200 rounded-lg flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-orange-600" />
            <p className="text-orange-800 text-xs font-medium">{error}</p>
          </div>
        )}
        
        <div className="grid gap-3">
          {news.length > 0 ? (
            news.map((item) => (
              <NewsCard key={item.id} item={item} />
            ))
          ) : (
            <div className="text-center py-6">
              <Globe className="w-10 h-10 text-gray-400 mx-auto mb-3" />
              <p className="text-gray-600 dark:text-gray-400 text-sm font-medium">
                No recent Nepal weather news available from RSS feeds
              </p>
            </div>
          )}
        </div>
        
        <div className="mt-4 pt-3 border-t border-gray-200 dark:border-gray-700">
          <p className="text-xs text-gray-500 text-center font-medium">
            Live news from Kantipur, Himalayan Times, Online Khabar, Republica, Setopati, Ratopati & Annapurna Post
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default WeatherNews;
