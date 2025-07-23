# API Configuration & CORS Setup

## ✅ What I Fixed

### 1. **Frontend axios URLs (useWeatherData.js)**
- ✅ **Fixed syntax error**: Removed extra 'e' on line 10
- ✅ **Added configurable API base URL**: Uses environment variable `VITE_API_URL`
- ✅ **Added timeout & headers**: 10-second timeout with proper headers
- ✅ **Better error handling**: More specific error messages for different failure types

### 2. **Environment Configuration**
- ✅ **Created frontend/.env**: Sets `VITE_API_URL=http://localhost:8000`
- ✅ **Updated Django CORS**: Added support for both dev (5173) and prod (3000) ports
- ✅ **Added ALLOWED_HOSTS**: Allows localhost, 127.0.0.1, and 0.0.0.0 for Docker

### 3. **Current API Endpoints**
```javascript
// Now uses Vite's import.meta.env (correct syntax for Vite projects)
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// All requests go to:
${API_BASE_URL}/api/current-weather/?${queryParam}
${API_BASE_URL}/api/aqi/?${queryParam}
${API_BASE_URL}/api/forecast/?${queryParam}
```

## 🔧 CORS Configuration

### Django Backend (settings.py)
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173", # Vite dev server
    "http://127.0.0.1:5173", 
    "http://localhost:3000",  # Production nginx
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
```

## 🚀 For Your Team

### Local Development
1. **Frontend**: Runs on `http://localhost:5173` (Vite)
2. **Backend**: Runs on `http://localhost:8000` (Django)
3. **CORS**: ✅ Properly configured for cross-origin requests

### With Docker
1. **Frontend**: `http://localhost:3000` (nginx)
2. **Backend**: `http://localhost:8000` (Django)
3. **Internal Docker**: Services communicate via container names

### Environment Variables
- Create `frontend/.env` with:
  ```
  VITE_API_URL=http://localhost:8000
  VITE_ENV=development
  ```
- **Important**: Vite requires the `VITE_` prefix for frontend access via `import.meta.env`
- For production, change `VITE_API_URL` to your actual domain

## 🐛 Troubleshooting CORS Issues

If you see CORS errors in browser console:

1. **Check Django is running**: `python manage.py runserver`
2. **Verify CORS middleware**: Should be high up in `MIDDLEWARE` list
3. **Check ports**: Frontend and backend on correct ports
4. **Browser cache**: Hard refresh (Ctrl+F5) or clear cache
5. **Check Network tab**: See if requests are actually being made

## ✅ Testing
- Open browser developer tools → Network tab
- Make a request from frontend
- Should see successful requests to `http://localhost:8000/api/...`
- No CORS errors in console
