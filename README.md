# 🌤️ WeatherWave-WebApp

A **Progressive Web App (PWA)** for weather forecasting with full offline support, intelligent caching, and ML-powered predictions for all 75 districts of Nepal.

---

## 🌟 Key Features

### 📱 **Progressive Web App (PWA)**
- **🔌 Full Offline Support**: Works completely without internet
- **📲 Installable**: Add to home screen on mobile/desktop
- **⚡ Lightning Fast**: Smart caching with 5-minute data freshness
- **🎨 Native Feel**: Standalone app experience

### 🌤️ **Weather Intelligence**
- **🌡️ Real-time Weather**: Temperature, humidity, wind, precipitation for 75 districts
- **📅 5-Day Forecast**: Detailed daily predictions with highs/lows
- **🏭 Air Quality**: PM2.5, PM10, and overall AQI monitoring
- **🤖 ML Predictions**: AI-powered next-day temperature forecasting
- **⚠️ Weather Alerts**: Severe weather notifications for Nepal

### 🔐 **User Experience**
- **🔑 Secure Authentication**: Knox token-based login system
- **⭐ Favorites Management**: Save and manage preferred locations
- **🌓 Theme Support**: Dark/light mode with system preference
- **📱 Responsive Design**: Optimized for all screen sizes
- **🔄 Unit Conversion**: Celsius/Fahrenheit toggle

---

## 🚀 Quick Start for PWA Experience

### **For Teammates - Experience Full PWA Features:**

```bash
# 1. Clone and setup
git clone https://github.com/DipeshJungThapa/WeatherWave-WebApp.git
cd WeatherWave-WebApp/frontend
npm install && npm run dev

# 2. Setup backend (for initial data)
cd ../backend
pip install -r requirements.txt
python manage.py runserver

# 3. Open http://localhost:5173 in browser
# 4. Create account → Browse districts → Test offline mode!
```

### **📱 Install as PWA:**
- **Desktop**: Click install icon in address bar
- **Mobile**: "Add to Home Screen" from browser menu
- **Result**: Standalone app experience with offline support

### **🔌 Test Offline Mode:**
1. **Load some weather data** by visiting different districts
2. **Disconnect internet** or use DevTools → Network → Offline
3. **Refresh page** - app still works with cached data!
4. **See offline indicator** and cached weather information

📖 **Detailed Guide**: [PWA & Offline Setup Guide](./docs/PWA_OFFLINE_GUIDE.md)

---

## 🗂️ Repository Structure

```
WeatherWave-WebApp/
├── backend/                # Django REST API
│   ├── manage.py
│   ├── weatherwave_project/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── forecast/
│   │   ├── __init__.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── models.py
│   │   └── serializers.py
│   └── requirements.txt
├── frontend/               # React + Vite + Tailwind (PWA)
│   └── (React app files)
├── ml/                     # ML pipeline and models
│   ├── data/               # Raw & intermediate CSVs (gitignored)
│   ├── models/             # Saved models & encoders (gitignored)
│   ├── steps/              # Preprocessing & training scripts
│   │   ├── 01_filter_recent.py
│   │   ├── 02_clean_basic.py
│   │   ├── 03_add_target_column.py
│   │   ├── 04_drop_missing.py
│   │   ├── 05_encode_district.py
│   │   ├── 06_train_model.py
│   │   └── 07_predict.py
│   └── requirements.txt
├── docs/                   # Documentation and proposals
├── .gitignore
└── README.md
```

---

## 🌱 Branching Strategy

Our team follows a straightforward branching strategy for organized development:

| Branch | Purpose |
|--------|---------|
| `main` | Stable, production-ready code. Deployed when ready. |
| `dev` | Active development branch. All feature work is integrated here. |
| `feature/<name>-<task>` | Individual feature branches (e.g., `feature/ml-preprocessing-pipeline`) |

### Feature Branch Workflow

1. **Always start by pulling the latest `dev`:**
   ```bash
   git fetch origin
   git checkout dev
   git pull origin dev
   ```

2. **Create a new feature branch off `dev`:**
   ```bash
   git checkout -b feature/<your-name>-<what-you-are-working-on>
   ```

3. **Work on your feature, then stage, commit, and push:**
   ```bash
   git add .
   git commit -m "feat: Implement <brief description>"
   git push origin feature/<your-name>-<what-you-are-working-on>
   ```

4. **Open a Pull Request on GitHub** against the `dev` branch

5. **Review and merge** after approval and testing

---

## 🚀 Getting Started

### 💻 Local Development Setup

#### 1. Clone & Setup
```bash
git clone https://github.com/<your-org>/WeatherWave-WebApp.git
cd WeatherWave-WebApp
git checkout dev
git pull origin dev
```

#### 2. 🛠️ Backend Setup
```bash
cd backend
python -m venv venv

# Activate virtual environment
source venv/bin/activate    # macOS/Linux
# OR
venv\Scripts\activate       # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver  # Runs on http://127.0.0.1:8000
```

#### 3. 💻 Frontend Setup

#### 👨‍💻 Development Mode (no PWA, no offline)
```bash
cd frontend
npm install
npm run dev
```
App runs at: http://localhost:5173

#### 📦 PWA Production Mode (with offline caching)
```bash
cd frontend
npm run build
npx serve dist
```
PWA runs at: http://localhost:3000
- Service worker activates
- Works offline
- You can install to home screen

#### 4. ML Pipeline Setup
```bash
cd ml
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Place raw_climate_data.csv in ml/data/
# Run the ML pipeline steps in order:
python steps/01_filter_recent.py
python steps/02_clean_basic.py
python steps/03_add_target_column.py
python steps/04_drop_missing.py
python steps/05_encode_district.py
python steps/06_train_model.py
python steps/07_predict.py
```

Final predictions will be saved in `ml/data/predictions.csv`

---

## 🌐 Environment Variables

### frontend/.env
```env
VITE_API_URL=http://localhost:8000
VITE_ENV=development
```

> **Note**: Vite requires environment variables to be prefixed with `VITE_` to be accessible in the frontend code via `import.meta.env.VITE_*`

### backend/.env (optional)
```env
WEATHER_API_KEY=your_openweather_key
OPENWEATHER_API_KEY=your_openweather_key
```

---

## 📡 API Endpoints

The backend provides the following REST API endpoints:

| Endpoint | Description |
|----------|-------------|
| `GET /api/current-weather/` | Current weather data |
| `GET /api/aqi/` | Air Quality Index |
| `GET /api/forecast/` | 5-day weather forecast |
| `POST /api/predict/` | ML-based temperature prediction |
| `POST /login/` | User login (Knox Auth) |
| `POST /register/` | User signup |
| `GET/POST/DELETE /api/favourites/` | Manage favorite cities |
| `GET /api/alerts?region={region}` | Severe weather alerts for Nepal |

---

## 🏗️ Technology Stack

**Frontend:**
- React.js + Vite + Tailwind CSS
- Service Workers for PWA functionality
- Responsive design with offline support

**Backend:**
- Django with Django REST Framework
- Knox authentication for secure user sessions
- SQLite (development) / PostgreSQL (production)

**Machine Learning:**
- Python with pandas, scikit-learn
- Random Forest Regressor for temperature prediction
- joblib for model serialization

**Deployment:**
- Frontend: Netlify
- Backend: Heroku/Render

---

## 🧠 ML Integration

The ML model predicts next-day temperature using historical weather data from Nepal.

- `ml/steps/` contains the complete training pipeline
- Outputs: `weather_model.pkl`, `label_encoder.pkl`
- Exposed via `/api/predict/` endpoint

### ML Pipeline Details

The ML pipeline consists of 7 sequential steps:

1. **01_filter_recent.py**: Keep only 2017–2019 data
2. **02_clean_basic.py**: Basic type cleaning, drop all-blank rows
3. **03_add_target_column.py**: Create `Temp_2m_tomorrow` target variable
4. **04_drop_missing.py**: Drop rows with any missing values
5. **05_encode_district.py**: Label-encode `District`; save encoder
6. **06_train_model.py**: Train & evaluate `RandomForestRegressor`; save model
7. **07_predict.py**: Load model & encoder, make predictions, save results

### ✅ Coming soon:
- Retraining pipeline
- Model versioning
- Auto-refresh on new data

*All raw data and models are ignored by Git; run scripts locally to regenerate.*

---

## 🧪 How to Test Offline

1. Open http://localhost:3000
2. Dev Tools → Application → Service Worker → Check "Offline"
3. Refresh → You'll still see cached data
4. Data is also stored in localStorage for fallback!

---

## ✅ Features Implemented

- ✅ **Login / Logout (Knox-based authentication)**
- ✅ **Fetch data using geolocation or manual city selection**
- ✅ **Add/remove favorite districts**
- ✅ **PWA support: installable + offline caching**
- ✅ **Current weather card with real-time data**
- ✅ **5-day forecast card with precipitation probability**
- ✅ **Air Quality Index (AQI) card**
- ✅ **ML-based temperature prediction**
- ✅ **Responsive design for all devices**
- ✅ **Severe weather alerts for Nepal**
- ✅ **User preferences (°C/°F toggle, light/dark theme)**

---

## 🤝 Team Members

- **Dipesh Thapa** (Team Lead, Frontend, ML Integration)
- **Aryam Ghimire** (ML Engineer)
- **Prashanna Chand** (Backend Developer)
- **Tathastu Subedi** (UI/UX Designer & QA)

---

## 🤝 Contributing

- Create feature branches off `dev` for each task
- Commit early, push often, open PRs for feedback
- Assign reviews and merge when approved
- Keep `dev` stable; merge to `main` only for releases

---

*WeatherWave-WebApp: Bringing reliable, localized weather intelligence to Nepal—online or offline.* 🇳🇵