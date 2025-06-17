# 🌤️ WeatherWave-WebApp

A responsive, PWA-enabled weather application for Nepal that combines real-time weather, AQI, and smart ML-based next-day temperature predictions.

---

## 📋 Project Overview

**WeatherWave** is a smart, responsive weather forecasting web app tailored for Nepal. It provides:
- Real-time current weather (temperature, humidity, wind speed, precipitation)
- 5-day forecast with daily highs/lows and precipitation probability
- Air Quality Index (AQI) data (PM2.5, PM10, overall index)
- ML-based next-day temperature prediction using Random Forest
- Offline access with PWA caching capabilities
- District selector with dropdown + autocomplete for 62 Nepali districts
- Severe weather alerts for Nepal (floods, landslides)
- User preferences (°C/°F toggle, light/dark theme)

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
├── frontend/               # React PWA UI
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

## 🚀 Getting Started (Local Setup)

### 1. Clone & Setup
```bash
git clone https://github.com/<your-org>/WeatherWave-WebApp.git
cd WeatherWave-WebApp
git checkout dev
git pull origin dev
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start      # Runs on http://localhost:3000
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv

# Activate virtual environment
source venv/bin/activate    # macOS/Linux
# OR
venv\Scripts\activate       # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver  # Runs on http://localhost:8000
```

### 4. ML Pipeline Setup
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

## 🛠️ API Endpoints

The backend provides the following REST API endpoints:

- `GET /api/hello/` - Health check endpoint
- `GET /api/weather?city={cityName}` - Current weather data
- `GET /api/forecast?city={cityName}` - 5-day weather forecast
- `GET /api/aqi?city={cityName}` - Air quality information
- `POST /api/predict` - ML-based temperature prediction
- `GET /api/alerts?region={region}` - Severe weather alerts for Nepal

---

## 🏗️ Technology Stack

**Frontend:**
- React.js with CSS Modules
- Service Workers for PWA functionality
- Responsive design

**Backend:**
- Django with Django REST Framework
- SQLite (development) / PostgreSQL (production)

**Machine Learning:**
- Python with pandas, scikit-learn
- Random Forest Regressor for temperature prediction
- joblib for model serialization


---

## 📦 ML Pipeline Details

The ML pipeline consists of 7 sequential steps:

1. **01_filter_recent.py**: Keep only 2017–2019 data
2. **02_clean_basic.py**: Basic type cleaning, drop all-blank rows
3. **03_add_target_column.py**: Create `Temp_2m_tomorrow` target variable
4. **04_drop_missing.py**: Drop rows with any missing values
5. **05_encode_district.py**: Label-encode `District`; save encoder
6. **06_train_model.py**: Train & evaluate `RandomForestRegressor`; save model
7. **07_predict.py**: Load model & encoder, make predictions, save results

*All raw data and models are ignored by Git; run scripts locally to regenerate.*

---

## 🤝 Team Members

- **Dipesh Thapa** (Frontend, ML Integration)
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

