"""
Simple Local Model Training for API Comparison
==============================================
Train model locally without cloud dependencies
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Constants
DATA_FILE = "encoded_districts.csv"
RANDOM_STATE = 42
TEST_SIZE = 0.2

MODEL_FEATURES = [
    'Latitude', 'Longitude', 'Precip', 'Pressure', 'Humidity_2m', 'RH_2m',
    'Temp_2m', 'WetBulbTemp_2m', 'MaxTemp_2m', 'MinTemp_2m', 'EarthSkinTemp',
    'WindSpeed_10m', 'MaxWindSpeed_10m', 'MinWindSpeed_10m',
    'WindSpeed_50m', 'MaxWindSpeed_50m', 'MinWindSpeed_50m',
    'District_encoded'
]

print("📊 Loading dataset...")
df = pd.read_csv(DATA_FILE)
print(f"Total samples: {len(df):,}")

# Prepare features and target
X = df[MODEL_FEATURES]
y = df['Temp_2m_tomorrow']

# Split data (same as original)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
)

print(f"Train: {len(X_train):,} samples")
print(f"Test: {len(X_test):,} samples")

# Train model (same config as original)
print("\n🔧 Training Random Forest model...")
model = RandomForestRegressor(
    n_estimators=5,
    random_state=RANDOM_STATE,
    n_jobs=-1
)

import time
start = time.time()
model.fit(X_train, y_train)
training_time = time.time() - start

print(f"✅ Model trained in {training_time:.2f} seconds")

# Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"\n📊 Model Performance:")
print(f"   MAE: {mae:.4f}°C")
print(f"   RMSE: {rmse:.4f}°C")
print(f"   R²: {r2:.4f}")

# Save model
print("\n💾 Saving model...")
joblib.dump(model, "trained_model.pkl")
print("   Saved: trained_model.pkl")
