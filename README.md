# 🌤️ WeatherWave-WebApp
A Progressive Web App (PWA) for weather forecasting with full offline support and ML-powered predictions for all 75 districts of Nepal.

---

## 🚀 Quick Start

### For Teammates — Experience Full PWA Features

### 1️⃣ Clone and Setup
```bash
git clone https://github.com/DipeshJungThapa/WeatherWave-WebApp.git
cd WeatherWave-WebApp
```

---

## 🖥️ Backend Setup (Django)
```bash
cd backend
python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🎨 Frontend Setup (React + Vite)
_Open a new terminal:_
```bash
cd ../frontend
npm install
npm run build && npx serve dist
```

---

## 📱 Install as PWA
- Desktop: Click the install icon in the address bar  
- Mobile: Choose "Add to Home Screen" from browser menu  
- Open: **http://localhost:3000**

---

## 🔌 Test Offline Mode
1. Load weather data while online  
2. Turn off internet or use DevTools → Network → Offline  
3. Refresh page  
4. App works offline using cached data  

---

## 🗂️ Project Structure
```
WeatherWave-WebApp/
├── backend/                 # Django REST API
├── frontend/                # React + Vite PWA
├── ml/                      # ML pipeline & models
└── docs/                    # Documentation
```

---

## 🌟 Core Features

### 📱 PWA Capabilities
- Full offline support  
- Installable on any device  
- Smart 5-minute caching  
- Native app-like experience  

### 🌤️ Weather Intelligence
- Real-time data for all 75 districts  
- 5-day forecast  
- AQI monitoring  
- ML temperature prediction  
- Severe weather alerts  

---

## 🛠️ Tech Stack
- **Frontend:** React, Vite, Tailwind CSS, PWA  
- **Backend:** Django REST Framework, Knox Auth  
- **ML:** Python, scikit-learn, pandas  
- **Deployment:** Netlify + Heroku/Render  

---

## 📡 API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/current-weather/` | GET | Current weather |
| `/api/forecast/` | GET | 5-day forecast |
| `/api/aqi/` | GET | Air Quality Index |
| `/api/predict/` | POST | ML temp prediction |
| `/login/` | POST | User authentication |
| `/api/favourites/` | GET/POST/DELETE | Manage favorites |

---

## 🤝 Team
- **Dipesh Thapa** — Team Lead, Frontend, ML  
- **Aryam Ghimire** — ML Engineer  
- **Prashanna Chand** — Backend Developer  
- **Tathastu Subedi** — UI/UX, QA  

---

## 🌱 Development Workflow
```bash
git checkout dev && git pull origin dev

git checkout -b feature/your-name-task

git add .
git commit -m "feat: description"
git push origin feature/your-name-task
```

Branch flow:  
`main (stable) ← dev (development) ← feature/* (tasks)`

---

## 🇳🇵 WeatherWave-WebApp
**Reliable weather intelligence for Nepal — online or offline.**
