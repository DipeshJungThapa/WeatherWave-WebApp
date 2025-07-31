# 🎨 WeatherWave Frontend Architecture & Implementation

## 📋 Table of Contents
- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Core Architecture](#core-architecture)
- [Component System](#component-system)
- [State Management](#state-management)
- [Routing & Navigation](#routing--navigation)
- [UI/UX Design System](#uiux-design-system)
- [PWA Implementation](#pwa-implementation)
- [Data Management](#data-management)
- [Authentication Flow](#authentication-flow)
- [Offline Capabilities](#offline-capabilities)
- [Performance Optimization](#performance-optimization)
- [Build & Deployment](#build--deployment)

---

## 🌟 Overview

The WeatherWave frontend is a modern, responsive React application built with cutting-edge technologies. It delivers a seamless weather forecasting experience with offline support, real-time data, and Progressive Web App (PWA) capabilities specifically designed for Nepal's diverse geographic regions.

### Key Features
- **Progressive Web App**: Installable, offline-first experience
- **Responsive Design**: Optimized for all devices (mobile, tablet, desktop)
- **Real-time Weather Data**: Live updates with intelligent caching
- **Offline Support**: Complete functionality without internet connection
- **Modern UI**: Clean, intuitive interface with dark/light theme support
- **Advanced Caching**: Intelligent data management for optimal performance

---

## 🔧 Technology Stack

### Core Framework & Libraries
- **React 18.2.0**: Modern functional components with hooks
- **Vite 4.0.0**: Next-generation frontend build tool
- **React Router DOM 7.7.1**: Client-side routing and navigation
- **TypeScript Support**: Type-safe development environment

### UI Framework & Styling
- **Tailwind CSS 3.4.3**: Utility-first CSS framework
- **Radix UI**: Accessible, unstyled UI primitives
  - `@radix-ui/react-dialog`: Modal and dialog components
  - `@radix-ui/react-dropdown-menu`: Dropdown functionality
  - `@radix-ui/react-tabs`: Tab navigation components
  - `@radix-ui/react-select`: Advanced select components
- **Lucide React 0.525.0**: Modern icon library
- **Framer Motion 12.23.0**: Advanced animations and transitions

### State Management & Data
- **React Context API**: Global state management
- **Axios 1.10.0**: HTTP client for API communication
- **Custom Hooks**: Reusable state logic encapsulation

### Development Tools & Quality
- **ESLint 9.29.0**: Code linting and quality enforcement
- **PostCSS 8.5.6**: CSS processing and optimization
- **Autoprefixer 10.4.21**: CSS vendor prefix automation

### PWA & Offline Support
- **Vite PWA Plugin 1.0.2**: Progressive Web App capabilities
- **Service Workers**: Intelligent caching and offline functionality
- **Web App Manifest**: Native app-like installation

### Theme & Accessibility
- **Next Themes 0.4.6**: Advanced theme management (dark/light mode)
- **Class Variance Authority 0.7.1**: Dynamic component styling
- **CLSX 2.1.1**: Conditional className utility

---

## 📁 Project Structure

```
frontend/
├── public/                          # Static assets
│   ├── manifest.webmanifest         # PWA manifest
│   ├── background.jpg               # App background
│   ├── pws-192-192-removebg-preview.png  # PWA icon (192x192)
│   ├── pws-512-512-removebg-preview.png  # PWA icon (512x512)
│   └── weatherwave-logo-removebg-preview.png
├── src/                             # Source code
│   ├── main.jsx                     # Application entry point
│   ├── App.jsx                      # Root component
│   ├── index.css                    # Global styles
│   ├── App.css                      # Component-specific styles
│   ├── components/                  # Reusable components
│   │   ├── ui/                      # Base UI components
│   │   │   ├── alert.jsx            # Alert/notification components
│   │   │   ├── button.jsx           # Button variants
│   │   │   ├── card.jsx             # Card layouts
│   │   │   ├── dialog.jsx           # Modal dialogs
│   │   │   ├── input.jsx            # Form inputs
│   │   │   ├── skeleton.jsx         # Loading skeletons
│   │   │   └── ...                  # Additional UI primitives
│   │   ├── CurrentWeatherCard.jsx   # Current weather display
│   │   ├── AQICard.jsx              # Air quality index
│   │   ├── ForecastCard.jsx         # Weather forecast
│   │   ├── PredictionCard.jsx       # ML predictions
│   │   ├── Navbar.jsx               # Navigation component
│   │   ├── FavoriteLocations.jsx    # Favorites management
│   │   ├── OfflineIndicator.jsx     # Offline status indicator
│   │   ├── WeatherNews.jsx          # Weather news component
│   │   ├── ZoomEarthHeatmap.jsx     # Interactive weather map
│   │   └── theme-provider.jsx       # Theme context provider
│   ├── pages/                       # Page components
│   │   ├── Dashboard.jsx            # Main dashboard
│   │   ├── AuthPageSimple.jsx       # Authentication page
│   │   └── ProfilePage.jsx          # User profile
│   ├── hooks/                       # Custom React hooks
│   │   ├── useWeatherData.js        # Weather data management
│   │   ├── useOnlineStatus.js       # Network status monitoring
│   │   ├── useAuthForm.js           # Authentication forms
│   │   ├── useGeolocation.js        # Location services
│   │   └── useFavourites.js         # Favorites management
│   ├── context/                     # React Context providers
│   │   └── AuthContext.jsx          # Authentication state
│   ├── services/                    # API services
│   │   └── authApi.js               # Authentication API calls
│   ├── config/                      # Configuration files
│   │   └── api.js                   # API endpoints configuration
│   ├── utils/                       # Utility functions
│   │   └── cacheUtils.js            # Caching utilities
│   ├── data/                        # Static data
│   │   └── nepalLocations.js        # Nepal districts data
│   ├── lib/                         # Library utilities
│   │   └── utils.js                 # Common utility functions
│   └── routes/                      # Route definitions
│       └── AppRouter.jsx            # Route configuration
├── .env                             # Environment variables
├── vite.config.js                   # Vite configuration
├── tailwind.config.js               # Tailwind CSS configuration
├── package.json                     # Dependencies and scripts
└── components.json                  # Shadcn/ui component configuration
```

---

## 🏗️ Core Architecture

### Component Hierarchy
```
App
├── AuthProvider (Context)
├── ThemeProvider (Context)
├── Router
└── Routes
    ├── Dashboard (Protected)
    │   ├── Navbar
    │   ├── CurrentWeatherCard
    │   ├── AQICard
    │   ├── ForecastCard
    │   ├── PredictionCard
    │   ├── ZoomEarthHeatmap
    │   ├── WeatherNews
    │   └── OfflineIndicator
    ├── AuthPageSimple
    ├── ProfilePage (Protected)
    └── FavoriteLocations (Protected)
```

### Data Flow Architecture
```
User Interaction → Component → Custom Hook → API Service → Backend
                                    ↓
Cache Management ← State Update ← Response Processing
                                    ↓
UI Re-render ← Context Update ← State Management
```

---

## 🧩 Component System

### 1. **UI Component Library** (`components/ui/`)

The application uses a comprehensive design system built on Radix UI primitives:

#### Core UI Components
```jsx
// Buttons with multiple variants
<Button variant="default" size="lg">Primary Action</Button>
<Button variant="outline" size="sm">Secondary Action</Button>

// Cards for content organization
<Card>
  <CardHeader>
    <CardTitle>Weather Information</CardTitle>
  </CardHeader>
  <CardContent>
    {/* Weather data */}
  </CardContent>
</Card>

// Alerts for notifications
<Alert variant="destructive">
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>Failed to fetch data</AlertDescription>
</Alert>
```

**Key Features**:
- **Accessibility First**: Full ARIA compliance and keyboard navigation
- **Theme Aware**: Automatic dark/light mode adaptation
- **Variant System**: Multiple styles through `class-variance-authority`
- **Composable**: Flexible component composition patterns

#### Advanced UI Patterns
```jsx
// Command palette for search
<Command>
  <CommandInput placeholder="Search locations..." />
  <CommandList>
    <CommandGroup heading="Nepal Districts">
      <CommandItem>Kathmandu</CommandItem>
      <CommandItem>Pokhara</CommandItem>
    </CommandGroup>
  </CommandList>
</Command>

// Tab navigation
<Tabs value={activeTab} onValueChange={setActiveTab}>
  <TabsList>
    <TabsTrigger value="weather">Weather</TabsTrigger>
    <TabsTrigger value="forecast">Forecast</TabsTrigger>
  </TabsList>
  <TabsContent value="weather">Current weather data</TabsContent>
</Tabs>
```

### 2. **Weather Components** (`components/`)

#### CurrentWeatherCard.jsx
**Purpose**: Displays real-time weather conditions
```jsx
const CurrentWeatherCard = ({ data, unit, onUnitChange }) => {
  // Features:
  // - Temperature display with unit conversion
  // - Weather icons and descriptions
  // - Additional metrics (humidity, pressure, wind)
  // - Responsive layout for all screen sizes
};
```

#### AQICard.jsx
**Purpose**: Air Quality Index visualization
```jsx
const AQICard = ({ data }) => {
  // Features:
  // - Color-coded AQI levels
  // - PM2.5 and PM10 readings
  // - Health recommendations
  // - Real-time quality assessment
};
```

#### ForecastCard.jsx
**Purpose**: 5-day weather forecast display
```jsx
const ForecastCard = ({ forecastData, unit }) => {
  // Features:
  // - Daily forecast cards
  // - Temperature trends
  // - Precipitation probability
  // - Weather condition icons
};
```

#### ZoomEarthHeatmap.jsx
**Purpose**: Interactive weather map for Nepal
```jsx
const NepalWeatherHeatmap = () => {
  // Features:
  // - Live weather layers (temperature, rainfall, wind)
  // - Nepal-focused geographic view
  // - Layer switching controls
  // - District navigation shortcuts
  // - Fullscreen support
};
```

### 3. **Navigation & Layout**

#### Navbar.jsx
**Purpose**: Application navigation and user interface
```jsx
const Navbar = ({ 
  currentDistrict, 
  setCurrentDistrict, 
  unit, 
  setUnit 
}) => {
  // Features:
  // - User authentication status
  // - Location selector dropdown
  // - Unit toggle (Celsius/Fahrenheit)
  // - Theme switcher (dark/light)
  // - Responsive mobile menu
};
```

---

## 📊 State Management

### 1. **Authentication Context** (`context/AuthContext.jsx`)

**Global Authentication State Management**:
```jsx
const AuthContext = createContext({
  isAuthenticated: false,
  user: null,
  token: null,
  login: () => {},
  logout: () => {},
  register: () => {}
});

// Authentication flow
const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  
  // Persistent authentication
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    if (storedToken && storedUser) {
      setUser(JSON.parse(storedUser));
      setToken(storedToken);
      setIsAuthenticated(true);
    }
  }, []);
};
```

**Features**:
- **Persistent Sessions**: Automatic login restoration
- **Secure Token Management**: Knox token integration
- **Global Access**: Available throughout the application
- **Automatic Cleanup**: Token removal on logout

### 2. **Custom Hooks for State Logic**

#### useWeatherData.js
**Purpose**: Comprehensive weather data management
```jsx
const useWeatherData = (location) => {
  const [weatherData, setWeatherData] = useState(null);
  const [aqiData, setAqiData] = useState(null);
  const [forecastData, setForecastData] = useState(null);
  const [predictionData, setPredictionData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isOffline, setIsOffline] = useState(false);
  const [isFromCache, setIsFromCache] = useState(false);
  
  // Intelligent caching strategy
  // Offline fallback mechanisms
  // Error handling and retry logic
  // Real-time data synchronization
};
```

**Advanced Features**:
- **Smart Caching**: 5-minute cache duration with fallback
- **Offline Support**: Graceful degradation when disconnected
- **Location Flexibility**: Support for city names and coordinates
- **Error Recovery**: Automatic retry and fallback mechanisms

#### useOnlineStatus.js
**Purpose**: Network connectivity monitoring
```jsx
const useOnlineStatus = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);
  
  return isOnline;
};
```

---

## 🛣️ Routing & Navigation

### Route Configuration (`App.jsx`)
```jsx
<Router>
  <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/login" element={<AuthPageSimple mode="login" />} />
    <Route path="/register" element={<AuthPageSimple mode="register" />} />
    <Route 
      path="/profile" 
      element={
        <ProtectedRoute>
          <ProfilePage />
        </ProtectedRoute>
      } 
    />
    <Route 
      path="/favorites" 
      element={
        <ProtectedRoute>
          <FavoriteLocations />
        </ProtectedRoute>
      } 
    />
  </Routes>
</Router>
```

### Protected Routes
**Purpose**: Authentication-based route protection
```jsx
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) return <Skeleton />;
  
  return isAuthenticated ? children : <Navigate to="/login" />;
};
```

**Features**:
- **Authentication Guards**: Automatic redirection for unauthenticated users
- **Loading States**: Skeleton loading during authentication checks
- **Seamless Navigation**: Smooth transitions between protected/public routes

---

## 🎨 UI/UX Design System

### 1. **Theme System** (`theme-provider.jsx`)

**Dark/Light Mode Implementation**:
```jsx
<ThemeProvider defaultTheme="system" storageKey="weatherwave-theme">
  <App />
</ThemeProvider>
```

**Features**:
- **System Preference Detection**: Automatic theme based on OS settings
- **Persistent Preferences**: Theme choice saved in localStorage
- **Smooth Transitions**: Animated theme switching
- **Component Awareness**: All components adapt automatically

### 2. **Responsive Design Strategy**

**Breakpoint System**:
```css
/* Tailwind CSS breakpoints */
sm: 640px    /* Mobile landscape / Small tablets */
md: 768px    /* Tablets */
lg: 1024px   /* Small desktops */
xl: 1280px   /* Large desktops */
2xl: 1536px  /* Extra large screens */
```

**Responsive Component Examples**:
```jsx
// Adaptive grid layouts
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Weather cards adapt to screen size */}
</div>

// Mobile-first navigation
<div className="hidden md:flex space-x-4">
  {/* Desktop navigation */}
</div>
<div className="md:hidden">
  {/* Mobile hamburger menu */}
</div>
```

### 3. **Color System & Accessibility**

**CSS Custom Properties** (`index.css`):
```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 221.2 83.2% 53.3%;
  --primary-foreground: 210 40% 98%;
  --secondary: 210 40% 96%;
  --muted: 210 40% 96%;
  --destructive: 0 84.2% 60.2%;
  --border: 214.3 31.8% 91.4%;
  --ring: 221.2 83.2% 53.3%;
}

[data-theme="dark"] {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  /* Dark mode color overrides */
}
```

**Accessibility Features**:
- **WCAG 2.1 Compliance**: AA level contrast ratios
- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Reader Support**: Proper ARIA labels and descriptions
- **Focus Management**: Visible focus indicators

---

## 📱 PWA Implementation

### 1. **Service Worker Configuration** (`vite.config.js`)

```javascript
VitePWA({
  registerType: 'autoUpdate',
  includeAssets: ['*.png', '*.svg'],
  manifest: {
    name: 'WeatherWave',
    short_name: 'WeatherWave',
    start_url: '/',
    display: 'standalone',
    theme_color: '#1e90ff',
    background_color: '#1e1e1e',
    icons: [
      {
        src: 'pws-192-192-removebg-preview.png',
        sizes: '192x192',
        type: 'image/png',
      },
      {
        src: 'pws-512-512-removebg-preview.png',
        sizes: '512x512',
        type: 'image/png',
      }
    ]
  },
  workbox: {
    globPatterns: ['**/*.{js,css,html,png,svg}']
  }
})
```

### 2. **Offline-First Strategy**

**Caching Hierarchy**:
1. **App Shell**: HTML, CSS, JS cached on first visit
2. **API Responses**: Weather data cached with TTL
3. **Static Assets**: Images and icons permanently cached
4. **Dynamic Content**: Intelligent cache-first strategy

**Cache Management** (`utils/cacheUtils.js`):
```javascript
export const cleanExpiredCache = () => {
  const keys = Object.keys(localStorage);
  const now = new Date().getTime();
  
  keys.forEach(key => {
    if (key.startsWith('weatherCache_')) {
      try {
        const cached = JSON.parse(localStorage.getItem(key));
        if (now - cached.timestamp > CACHE_DURATION) {
          localStorage.removeItem(key);
        }
      } catch (e) {
        localStorage.removeItem(key);
      }
    }
  });
};
```

### 3. **Installation Prompts**

**Native App Experience**:
- **Install Banner**: Automatic installation prompts
- **Standalone Mode**: Full-screen app experience
- **App Icons**: Custom branded icons for home screen
- **Splash Screen**: Branded loading experience

---

## 🔄 Data Management

### 1. **API Configuration** (`config/api.js`)

**Centralized Endpoint Management**:
```javascript
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export const API_ENDPOINTS = {
  CURRENT_WEATHER: '/api/current-weather/',
  FORECAST: '/api/forecast/',
  AQI: '/api/aqi/',
  PREDICT_CITY: '/api/predict-city/',
  ALERTS: '/api/alert/',
  FAVORITES: '/api/favorites/',
  REGISTER: '/register/',
  LOGIN: '/login/',
  USERS: '/users/',
  NEWS: '/api/news/',
  WEATHER_NEWS: '/api/weather-news/',
};

export const buildApiUrl = (endpoint, params = '') => {
  const url = `${API_BASE_URL}${endpoint}`;
  return params ? `${url}?${params}` : url;
};
```

### 2. **HTTP Client Configuration**

**Axios Integration with Authentication**:
```javascript
// Automatic token attachment
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Global error handling
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle authentication errors
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

### 3. **Smart Caching Strategy**

**Multi-Level Caching**:
```javascript
const fetchWithCache = async (url, cacheKey) => {
  // 1. Check localStorage cache
  const cached = localStorage.getItem(cacheKey);
  if (cached && !isExpired(cached)) {
    return JSON.parse(cached).data;
  }
  
  // 2. Fetch from API
  try {
    const response = await axios.get(url);
    
    // 3. Update cache
    localStorage.setItem(cacheKey, JSON.stringify({
      data: response.data,
      timestamp: Date.now()
    }));
    
    return response.data;
  } catch (error) {
    // 4. Fallback to stale cache if available
    if (cached) {
      return JSON.parse(cached).data;
    }
    throw error;
  }
};
```

---

## 🔐 Authentication Flow

### 1. **Login Process**
```jsx
const login = async (username, password) => {
  try {
    setLoading(true);
    const response = await authService.login(username, password);
    
    // Store authentication data
    localStorage.setItem('token', response.token);
    localStorage.setItem('user', JSON.stringify(response.user));
    
    // Update context state
    setToken(response.token);
    setUser(response.user);
    setIsAuthenticated(true);
    
    // Navigate to dashboard
    navigate('/dashboard');
  } catch (error) {
    setError(error.message);
  } finally {
    setLoading(false);
  }
};
```

### 2. **Persistent Authentication**
```jsx
// Automatic authentication restoration
useEffect(() => {
  const storedToken = localStorage.getItem('token');
  const storedUser = localStorage.getItem('user');
  
  if (storedToken && storedUser) {
    try {
      setUser(JSON.parse(storedUser));
      setToken(storedToken);
      setIsAuthenticated(true);
    } catch (error) {
      // Clear invalid data
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  }
  setLoading(false);
}, []);
```

### 3. **Secure Logout**
```jsx
const logout = () => {
  // Clear authentication data
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  
  // Reset context state
  setToken(null);
  setUser(null);
  setIsAuthenticated(false);
  
  // Navigate to login
  navigate('/login');
};
```

---

## 📶 Offline Capabilities

### 1. **Offline Detection** (`hooks/useOnlineStatus.js`)

**Real-time Network Monitoring**:
```jsx
const useOnlineStatus = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  
  useEffect(() => {
    const handleStatusChange = () => {
      setIsOnline(navigator.onLine);
    };
    
    window.addEventListener('online', handleStatusChange);
    window.addEventListener('offline', handleStatusChange);
    
    return () => {
      window.removeEventListener('online', handleStatusChange);
      window.removeEventListener('offline', handleStatusChange);
    };
  }, []);
  
  return isOnline;
};
```

### 2. **Offline Indicators** (`components/OfflineIndicator.jsx`)

**User-Friendly Offline Notifications**:
```jsx
const OfflineIndicator = ({ isOffline, isFromCache }) => {
  if (!isOffline) return null;
  
  return (
    <Alert className="mb-4 bg-yellow-100 border-yellow-300">
      <WifiOff className="h-4 w-4" />
      <AlertDescription>
        You're offline. {isFromCache ? 'Showing cached data.' : 'Limited functionality available.'}
      </AlertDescription>
    </Alert>
  );
};
```

### 3. **Graceful Degradation**

**Feature Availability Matrix**:
- ✅ **Always Available**: Cached weather data, basic navigation, user interface
- ⚠️ **Limited Offline**: Favorites (read-only), settings, theme switching
- ❌ **Online Only**: Real-time updates, new data fetching, user authentication

---

## ⚡ Performance Optimization

### 1. **Code Splitting & Lazy Loading**

**Route-Based Code Splitting**:
```jsx
const Dashboard = lazy(() => import('./pages/Dashboard'));
const ProfilePage = lazy(() => import('./pages/ProfilePage'));

// Wrapped in Suspense
<Suspense fallback={<Skeleton />}>
  <Routes>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/profile" element={<ProfilePage />} />
  </Routes>
</Suspense>
```

### 2. **Component Optimization**

**React.memo for Expensive Components**:
```jsx
const WeatherCard = React.memo(({ data, unit }) => {
  // Expensive weather calculations
  const processedData = useMemo(() => {
    return expensiveWeatherProcessing(data);
  }, [data]);
  
  return <Card>{/* Render weather data */}</Card>;
});
```

**Custom Hook Optimization**:
```jsx
const useWeatherData = (location) => {
  // Memoized location key generation
  const getLocationKey = useCallback((loc) => {
    if (typeof loc === 'string') return loc;
    if (typeof loc === 'object' && loc.lat && loc.lon) return `${loc.lat},${loc.lon}`;
    return 'default';
  }, []);
  
  // Dependency optimization
  useEffect(() => {
    fetchWeatherData();
  }, [location, getLocationKey, isOnline]);
};
```

### 3. **Bundle Optimization**

**Vite Configuration** (`vite.config.js`):
```javascript
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
          utils: ['axios', 'clsx', 'tailwind-merge']
        }
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

---

## 🚀 Build & Deployment

### 1. **Development Environment**

**Local Development Setup**:
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Development server runs on http://localhost:5173
```

**Environment Variables** (`.env`):
```bash
VITE_API_URL=http://localhost:8000
VITE_ENV=development
```

### 2. **Production Build**

**Build Process**:
```bash
# Create production build
npm run build

# Preview production build
npm run preview

# Build outputs to ./dist directory
```

**Build Optimization Features**:
- **Tree Shaking**: Dead code elimination
- **Minification**: CSS and JavaScript compression
- **Asset Optimization**: Image compression and optimization
- **Code Splitting**: Automatic chunk optimization
- **Service Worker**: PWA offline capabilities

### 3. **Deployment Strategy**

**Static Site Deployment**:
```bash
# Build for production
npm run build

# Deploy to static hosting (Netlify, Vercel, etc.)
# Copy ./dist directory contents to hosting platform
```

**PWA Installation**:
- **Web Server**: Serve over HTTPS for PWA features
- **Service Worker**: Automatic registration and updates
- **Manifest**: Proper PWA manifest configuration
- **Icons**: High-resolution icons for all platforms

---

## 🎯 Frontend's Role in WeatherWave Ecosystem

### Core Responsibilities
1. **User Interface**: Intuitive, responsive weather information display
2. **Data Visualization**: Interactive charts, maps, and weather graphics
3. **User Experience**: Seamless navigation and interaction design
4. **Offline Support**: Complete functionality without internet connection
5. **Performance**: Fast loading times and smooth interactions

### Integration Points
- **Backend API**: RESTful communication with Django backend
- **Authentication**: Secure token-based user authentication
- **Caching**: Intelligent local data storage and management
- **PWA Features**: Native app-like experience on all devices

### User Experience Metrics
- **First Contentful Paint**: <1.5s on 3G networks
- **Time to Interactive**: <3s for initial page load
- **Offline Functionality**: 100% feature availability with cached data
- **Accessibility Score**: 95+ Lighthouse accessibility rating
- **Mobile Performance**: 90+ Google PageSpeed Insights score

### Key Differentiators
- **Nepal-Specific Design**: Tailored for Nepali users and geography
- **Offline-First**: Complete functionality without internet
- **Progressive Enhancement**: Works on all devices and network conditions
- **Modern Architecture**: Latest React patterns and best practices
- **Accessibility Focus**: Inclusive design for all users

---

## 🔄 Data Flow Summary

### Complete Request Cycle
```
User Action → Component Event → Custom Hook → API Service → Backend
                                    ↓
Cache Check ← State Management ← Response Processing ← API Response
                                    ↓
UI Update ← Context Propagation ← State Update ← Cache Update
```

### Error Handling Strategy
- **Network Errors**: Automatic retry with exponential backoff
- **Authentication Errors**: Redirect to login with context preservation
- **Data Errors**: Fallback to cached data with user notification
- **UI Errors**: Error boundaries with graceful recovery options

---

*This documentation represents the comprehensive frontend architecture of WeatherWave, designed to deliver an exceptional weather forecasting experience with modern web technologies and best practices.* 🌤️
