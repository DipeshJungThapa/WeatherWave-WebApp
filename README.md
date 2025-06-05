# 🌤️ WeatherWave

**WeatherWave** is a smart, responsive weather forecasting web app tailored for Nepal. It provides:

- Real-time current weather (temperature, humidity, wind speed)
- 5-day forecast (daily highs/lows, precipitation probability)
- Air Quality Index (AQI) data (PM2.5, PM10, etc.)
- ML-based next-day temperature prediction (via `/api/predict` endpoint)
- Offline access (PWA caching)
- Severe weather alerts for Nepal (floods, landslides)

---

## 📁 Project Structure

```
weatherwave/
├── backend/
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
├── frontend/
│   └── (React app files)
├── ml/
│   ├── train_model.py
│   ├── predict_model.py
│   ├── model.pkl
│   └── requirements.txt
├── docs/
│   └── (Proposal PDFs, diagrams, etc.)
├── .gitignore
└── README.md
```

The project is organized into the following top-level directories:

* **`backend/`**
    * Contains a minimal Django project (`weatherwave_project/`) and the `forecast/` app.
    * Defines API endpoints such as `GET /api/weather?city={cityName}`, `POST /api/predict`, and `GET /api/aqi?city={cityName}`.
    * Includes `backend/requirements.txt` to install Django, Django REST Framework, and any auxiliary libraries.

* **`frontend/`**  
    * Houses the React UI (created via `create-react-app`).
    * Responsible for fetching data from backend endpoints and displaying it to users (real-time weather, five-day forecast, AQI, ML-predicted temperature, etc.).
    * Already initialized; run `npm install` and `npm start` from within this folder to launch the dev server.

* **`ml/`**
    * Contains Python scripts for training and saving the ML model (`train_model.py`) and for loading and using it (`predict_model.py`).
    * Includes `model.pkl` as the serialized Linear Regression (or other) model.
    * Contains `ml/requirements.txt` for Python packages such as `pandas`, `scikit-learn`, and `joblib`.

* **`docs/`**
    * All formal documentation, proposal files, architecture diagrams, and final reports live on the `docs` branch.
    * This folder on the `main`/`dev` branches can hold interim design files but may be kept empty until you merge from `docs` branch.

* **`.gitignore`**
    * Ignores Python caches, `venv/`, React `node_modules/`, build artifacts, and OS-specific files.

* **`README.md`** (This file!)

---

## 🌱 Branching Strategy

Our team follows a straightforward branching strategy for organized and collaborative development:

| Branch     | Purpose                                                             |
|------------|---------------------------------------------------------------------|
| `main`     | Stable, production-ready code. Deployed to Heroku (backend) and Netlify (frontend) when ready. |
| `dev`      | Active development branch. All feature work is integrated here. Once `dev` is validated end-to-end, it merges into `main`. |
| `docs`     | (Optional) Contains proposal, architecture diagrams, final report, and PDFs. **YO CHAI BANAKO XAINA, BANAYERA NI KAAM LAGCHA JASTO LAGENA SO..** |

### Feature Branch Workflow

Every new piece of work (feature, bug fix, experiment) must be developed on its own dedicated feature branch. This keeps our work isolated and prevents conflicts on shared branches.

1. **Always start by pulling the latest `dev`:**
    ```bash
    git fetch origin
    git checkout dev
    git pull origin dev
    ```

2. **Create a new feature branch off `dev`.** Name it clearly and logically:
    ```bash
    git checkout -b feature/<your-name>-<what-you-are-working-on>
    ```
    **Examples:**
    * `feature/prashanna-backend-api`
    * `feature/aryam-ml-training`
    * `feature/dipesh-frontend-ui`

3. **Work on your feature.** Make your changes, add new files, etc.

4. **Stage, commit, and push your branch to GitHub:**
    ```bash
    git add .
    git commit -m "feat: Implement <brief, descriptive message of your changes>"
    git push origin feature/<your-name>-<what-you-are-working-on>
    ```

5. **Open a Pull Request (PR) on GitHub:**
    * Go to your repository on GitHub.
    * GitHub will usually show a banner prompting you to open a PR for your newly pushed branch.
    * **Base branch:** Ensure this is set to `dev`.
    * **Compare branch:** This should be your `feature/<your-name>-<what-you-are-working-on>` branch.
    * Add a clear description of your changes.
    * Request a review (assign to Dipesh or another relevant teammate).

6. **Review and Merge:** Once the code is reviewed and approved (and any conflicts are resolved), it will be merged into the `dev` branch.

7. **Merging `dev` to `main`:** The `dev` branch will only be merged into `main` (by the team lead, Dipesh) when the code is thoroughly tested, stable, and ready for a new release.

---

## 🚀 Getting Started (Local Setup for Teammates)

Follow these steps to get your local environment set up and ready to contribute:

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/DipeshJungThapa/WeatherWave-WebApp.git
    cd WeatherWave-WebApp
    ```

2. **Checkout the `dev` branch:** This is where all active development work happens.
    ```bash
    git checkout dev
    git pull origin dev
    ```

3. **Create a feature branch:** Always work on a new branch for your tasks.
    ```bash
    git checkout -b feature/your-feature-name
    ```

4. **Begin working in your respective folder:**

    **Backend Developers (e.g., Prashanna):**
    ```bash
    cd backend
    python -m venv venv
    ```
    
    **Activate virtual environment:**
    ```bash
    # Windows (PowerShell or Git Bash)
    venv\Scripts\activate
    
    # macOS / Linux / WSL
    source venv/bin/activate
    ```
    
    **Install dependencies and run:**
    ```bash
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
    ```
    
    Backend API server runs at `http://localhost:8000/`.
    
    **Test the health endpoint:**
    ```bash
    curl http://localhost:8000/api/hello/
    # Should return: {"message": "WeatherWave backend is working!"}
    ```

    **Frontend Developers (e.g., Dipesh):**
    ```bash
    cd frontend
    npm install
    npm start
    ```
    
    Opens the React development server at `http://localhost:3000`.

    **ML Developers (e.g., Aryam):**
    ```bash
    cd ml
    python -m venv venv
    ```
    
    **Activate virtual environment:**
    ```bash
    # Windows
    venv\Scripts\activate
    
    # macOS / Linux / WSL
    source venv/bin/activate
    ```
    
    **Install ML dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    
    **Training (one-time):**
    ```bash
    python train_model.py
    # Loads historical data (e.g., weather_data.csv), trains a Linear Regression model, and saves model.pkl
    ```
    
    **Prediction (example):**
    ```bash
    python predict_model.py
    # Loads model.pkl and prints a sample next-day temperature
    ```

    **UI/UX & QA (e.g., Tathastu):**
    You can use the `frontend/` folder for wireframes or simple HTML prototypes. Focus on coordinating design, testing, and documentation.

5. **Push your code to your feature branch and open a Pull Request:** (See "Feature Branch Workflow" above for details).

---

## 🛠️ API Endpoints

The backend provides the following REST API endpoints:

* `GET /api/hello/` - Health check endpoint
* `GET /api/weather?city={cityName}` - Current weather data
* `GET /api/forecast?city={cityName}` - 5-day weather forecast  
* `GET /api/aqi?city={cityName}` - Air quality information
* `POST /api/predict` - ML-based temperature prediction
* `GET /api/alerts?region={region}` - Severe weather alerts for Nepal

---

## 🏗️ Technology Stack

**Frontend:**
* React.js
* CSS3/SCSS  
* PWA capabilities
* Responsive design

**Backend:**
* Django
* Django REST Framework
* SQLite/PostgreSQL
* Python 3.8+

**Machine Learning:**
* scikit-learn
* pandas
* NumPy
* joblib

**Deployment:**
* Backend: Heroku
* Frontend: Netlify
* Database: PostgreSQL (production)

---
## Initially Do This

* Clone the repo
* Checkout dev
* Create their own feature branch
* Install dependencies in the correct folder
* Run each component locally
* Push changes and open PRs against dev

## 👥 Team Members

* **Dipesh Thapa** (Team Lead, Frontend, ML Integration)
* **Aryam Ghimire** (ML Engineer)  
* **Prashanna Chand** (Backend Developer)
* **Tathastu Subedi** (UI/UX Designer & QA)

---

**Good luck kta hoo!** 🇳🇵