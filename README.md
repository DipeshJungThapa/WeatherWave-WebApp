# 🌤️ WeatherWave
**WeatherWave** is a smart, responsive weather forecasting web app tailored for Nepal. It provides:
- Real-time current weather (temperature, humidity, wind speed)
- 5-day forecast (daily highs/lows, precipitation probability)
- Air Quality Index (AQI) data (PM2.5, PM10, etc.)
- ML-based next-day temperature prediction (via `/predict` endpoint)
- Offline access (PWA caching)
- Severe weather alerts for Nepal (floods, landslides)

---
## 📁 Project Structure
The project is organized into the following top-level directories:

* **`backend/`**
    * Contains the Django project and app(s).
    * Defines API endpoints (e.g., `GET /api/weather?city={cityName}`, `GET /api/aqi?city={cityName}`, `POST /api/predict`).
* **`frontend/`**
    * Will house the HTML/JS or React + Tailwind CSS UI.
    * Responsible for fetching data from backend endpoints and displaying weather, forecast, ML predictions, AQI, and alerts.
* **`ml/`**
    * Includes machine learning model training scripts (e.g., `data_preprocess.py`), Jupyter notebooks (e.g., `train_model.ipynb`), and saved model files (e.g., `model.pkl`).
* **`docs/`**
    * Intended for documentation, architecture diagrams, and final proposal PDFs. While primary documentation can live on a separate `docs` branch, this folder on `dev` can hold shared artifacts.
* **`.gitignore`**
* **`README.md`** (This file!)

---
## 🌱 Branching Strategy

Our team will follow a clear branching strategy to ensure organized and collaborative development:

| Branch     | Purpose                                                             |
|------------|---------------------------------------------------------------------|
| `main`     | Always stable, production-ready code. This branch will only contain fully tested and deployable versions of the application. |
| `dev`      | This is our primary active development and integration branch. All new features and bug fixes will be merged into `dev` via Pull Requests. |
| `docs`     | (Optional for this project) This branch would contain proposal, architecture diagrams, final report, and PDFs.  *** YO CHAI BANAKO XAINA, BANAYERA NI KAAM LAGCHA       | JASTO LAGENA SO.. **|

### Feature Branch Workflow

Every new piece of work (feature, bug fix, experiment) must be developed on its own dedicated feature branch. This keeps our work isolated and prevents conflicts on shared branches.

1.  **Always start by pulling the latest `dev`:**
    ```bash
    git fetch origin
    git checkout dev
    git pull origin dev
    ```
2.  **Create a new feature branch off `dev`.** Name it clearly and logically:
    ```bash
    git checkout -b feature/<your-name>-<what-you-are-working-on>
    ```
    * **Examples:**
        * `feature/prashanna-backend-weather-api`
        * `feature/aryam-ml-train-model`
        * `feature/dipesh-frontend-ui-layout`
3.  **Work on your feature.** Make your changes, add new files, etc.
4.  **Stage, commit, and push your branch to GitHub:**
    ```bash
    git add .
    git commit -m "feat: Implement <brief, descriptive message of your changes>"
    git push origin feature/<your-name>-<what-you-are-working-on>
    ```
5.  **Open a Pull Request (PR) on GitHub:**
    * Go to your repository on GitHub.
    * GitHub will usually show a banner prompting you to open a PR for your newly pushed branch.
    * **Base branch:** Ensure this is set to `dev`.
    * **Compare branch:** This should be your `feature/<your-name>-<what-you-are-working-on>` branch.
    * Add a clear description of your changes.
    * Request a review (assign to Dipesh or another relevant teammate).
6.  **Review and Merge:** Once the code is reviewed and approved (and any conflicts are resolved), it will be merged into the `dev` branch.
7.  **Merging `dev` to `main`:** The `dev` branch will only be merged into `main` (by the team lead, Dipesh) when the code is thoroughly tested, stable, and ready for a new release.

---
## 🚀 Getting Started (Local Setup for Teammates)

Follow these steps to get your local environment set up and ready to contribute:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/weatherwave-webapp.git](https://github.com/YOUR_USERNAME/weatherwave-webapp.git)
    cd weatherwave-webapp
    ```
2.  **Checkout the `dev` branch:** This is where all active development work happens.
    ```bash
    git checkout dev
    ```
3.  **Pull the latest changes to `dev`:**
    ```bash
    git pull origin dev
    ```
4.  **Create a feature branch:** Always work on a new branch for your tasks.
    ```bash
    git checkout -b feature/your-feature-name
    ```
5.  **Begin working in your respective folder:**

    * **Backend Developers (e.g., Prashanna):**
        ```bash
        cd backend
        python -m venv venv
        source venv/Scripts/activate    # (Windows) or `source venv/bin/activate` (macOS/Linux)
        pip install django djangorestframework
        # Then start your Django project/app
        ```
    * **Frontend Developers (e.g., Dipesh):**
        ```bash
        cd frontend
        npm init -y
        npm install tailwindcss postcss autoprefixer
        npx tailwindcss init
        # Then start building your UI
        ```
    * **ML Developers (e.g., Aryam):**
        ```bash
        cd ml
        python -m venv venv
        source venv/Scripts/activate
        pip install pandas scikit-learn joblib jupyter
        # Then start with data preprocessing or model training
        ```
    * **UI/UX & QA (e.g., Tathastu):**
        You can use the `frontend/` folder for wireframes or simple HTML prototypes. Focus on coordinating design, testing, and documentation.

6.  **Push your code to your feature branch and open a Pull Request:** (See "Feature Branch Workflow" above for details).

---
## 👥 Team Members

* **Dipesh Thapa** (Team Lead, Frontend, ML Integration)
* **Aryam Ghimire** (ML)
* **Prashanna Chand** (Backend)
* **Tathastu Subedi** (UI/UX & QA)

---
**Good luck kta hoo!**