"""
Regional Performance Analysis - NO BLUFFING
Generates REAL metrics for paper revision
"""
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("🔍 REGIONAL PERFORMANCE ANALYSIS - GENERATING REAL NUMBERS")
print("="*70)

# Load data
print("\n📂 Loading data files...")
try:
    df = pd.read_csv('encoded_districts.csv')
    le = joblib.load('label_encoder.pkl')
    print(f"✅ Loaded {len(df):,} samples from encoded_districts.csv")
    print(f"✅ Loaded label encoder with {len(le.classes_)} districts")
except Exception as e:
    print(f"❌ Error loading files: {e}")
    print("   Make sure encoded_districts.csv and label_encoder.pkl are in project root")
    exit(1)

# Check columns
print(f"\n📊 Dataset shape: {df.shape}")
print(f"   Columns: {list(df.columns)}")

# Define features (from your actual model)
MODEL_FEATURES = [
    'Latitude', 'Longitude', 'Precip', 'Pressure', 'Humidity_2m', 'RH_2m',
    'Temp_2m', 'WetBulbTemp_2m', 'MaxTemp_2m', 'MinTemp_2m', 'EarthSkinTemp',
    'WindSpeed_10m', 'MaxWindSpeed_10m', 'MinWindSpeed_10m',
    'WindSpeed_50m', 'MaxWindSpeed_50m', 'MinWindSpeed_50m',
    'District_encoded'
]

TARGET = 'Temp_2m_tomorrow'

# Verify columns exist
missing_features = [f for f in MODEL_FEATURES if f not in df.columns]
if missing_features:
    print(f"❌ Missing features: {missing_features}")
    exit(1)

if TARGET not in df.columns:
    print(f"❌ Target column '{TARGET}' not found")
    exit(1)

print(f"✅ All {len(MODEL_FEATURES)} features present")

# Prepare data
print("\n🔧 Preparing train/test split (80/20, random_state=42)...")
X = df[MODEL_FEATURES].astype('float32')
y = df[TARGET].astype('float32')

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"   Train samples: {len(X_train):,}")
print(f"   Test samples: {len(X_test):,}")

# Train model (same config as paper)
print("\n🤖 Training Random Forest model (n_estimators=5)...")
model = RandomForestRegressor(
    n_estimators=5,
    random_state=42,
    n_jobs=-1
)

import time
start_time = time.time()
model.fit(X_train, y_train)
training_time = time.time() - start_time

print(f"✅ Model trained in {training_time:.2f} seconds")

# Predict on test set
print("\n🎯 Generating predictions on test set...")
y_pred = model.predict(X_test)

# Calculate overall metrics
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n" + "="*70)
print("📊 OVERALL PERFORMANCE (Test Set)")
print("="*70)
print(f"MAE:  {mae:.4f} °C")
print(f"RMSE: {rmse:.4f} °C")
print(f"R²:   {r2:.4f}")

# Get test set with predictions
test_df = df.iloc[X_test.index].copy()
test_df['predicted'] = y_pred
test_df['actual'] = y_test.values
test_df['error'] = np.abs(test_df['actual'] - test_df['predicted'])

# District metadata (from your actual code)
district_metadata = {
    "Achham": {"region": "Mountain", "elevation": 2900, "province": "Sudurpashchim"},
    "Arghakhanchi": {"region": "Hill", "elevation": 2000, "province": "Lumbini"},
    "Baglung": {"region": "Hill", "elevation": 2700, "province": "Gandaki"},
    "Baitadi": {"region": "Mountain", "elevation": 2900, "province": "Sudurpashchim"},
    "Bajhang": {"region": "Mountain", "elevation": 2900, "province": "Sudurpashchim"},
    "Bajura": {"region": "Mountain", "elevation": 2900, "province": "Sudurpashchim"},
    "Banke": {"region": "Terai", "elevation": 200, "province": "Lumbini"},
    "Bara": {"region": "Terai", "elevation": 100, "province": "Madhesh"},
    "Bardiya": {"region": "Terai", "elevation": 200, "province": "Lumbini"},
    "Bhaktapur": {"region": "Hill", "elevation": 1400, "province": "Bagmati"},
    "Bhojpur": {"region": "Hill", "elevation": 1700, "province": "Koshi"},
    "Chitwan": {"region": "Terai", "elevation": 200, "province": "Bagmati"},
    "Dadeldhura": {"region": "Hill", "elevation": 2500, "province": "Sudurpashchim"},
    "Dailekh": {"region": "Hill", "elevation": 2800, "province": "Karnali"},
    "Dang": {"region": "Terai", "elevation": 700, "province": "Lumbini"},
    "Darchula": {"region": "Mountain", "elevation": 3000, "province": "Sudurpashchim"},
    "Dhading": {"region": "Hill", "elevation": 2000, "province": "Bagmati"},
    "Dhankuta": {"region": "Hill", "elevation": 1200, "province": "Koshi"},
    "Dhanusha": {"region": "Terai", "elevation": 100, "province": "Madhesh"},
    "Dolakha": {"region": "Hill", "elevation": 2700, "province": "Bagmati"},
    "Dolpa": {"region": "Mountain", "elevation": 3600, "province": "Karnali"},
    "Doti": {"region": "Hill", "elevation": 2500, "province": "Sudurpashchim"},
    "East Rukum": {"region": "Hill", "elevation": 2600, "province": "Lumbini"},
    "Gorkha": {"region": "Hill", "elevation": 2400, "province": "Gandaki"},
    "Gulmi": {"region": "Hill", "elevation": 2500, "province": "Lumbini"},
    "Humla": {"region": "Mountain", "elevation": 3000, "province": "Karnali"},
    "Ilam": {"region": "Hill", "elevation": 1400, "province": "Koshi"},
    "Jajarkot": {"region": "Hill", "elevation": 2800, "province": "Karnali"},
    "Jhapa": {"region": "Terai", "elevation": 100, "province": "Koshi"},
    "Jumla": {"region": "Mountain", "elevation": 2500, "province": "Karnali"},
    "Kailali": {"region": "Terai", "elevation": 150, "province": "Sudurpashchim"},
    "Kalikot": {"region": "Mountain", "elevation": 2900, "province": "Karnali"},
    "Kanchanpur": {"region": "Terai", "elevation": 150, "province": "Sudurpashchim"},
    "Kapilvastu": {"region": "Terai", "elevation": 100, "province": "Lumbini"},
    "Kaski": {"region": "Hill", "elevation": 900, "province": "Gandaki"},
    "Kathmandu": {"region": "Hill", "elevation": 1400, "province": "Bagmati"},
    "Kavrepalanchok": {"region": "Hill", "elevation": 1600, "province": "Bagmati"},
    "Khotang": {"region": "Hill", "elevation": 2700, "province": "Koshi"},
    "Lalitpur": {"region": "Hill", "elevation": 1400, "province": "Bagmati"},
    "Lamjung": {"region": "Hill", "elevation": 2400, "province": "Gandaki"},
    "Mahottari": {"region": "Terai", "elevation": 100, "province": "Madhesh"},
    "Makwanpur": {"region": "Hill", "elevation": 1200, "province": "Bagmati"},
    "Manang": {"region": "Mountain", "elevation": 3540, "province": "Gandaki"},
    "Morang": {"region": "Terai", "elevation": 100, "province": "Koshi"},
    "Mugu": {"region": "Mountain", "elevation": 2900, "province": "Karnali"},
    "Mustang": {"region": "Mountain", "elevation": 3840, "province": "Gandaki"},
    "Myagdi": {"region": "Hill", "elevation": 2800, "province": "Gandaki"},
    "Nawalpur": {"region": "Terai", "elevation": 300, "province": "Gandaki"},
    "Nuwakot": {"region": "Hill", "elevation": 2000, "province": "Bagmati"},
    "Okhaldhunga": {"region": "Hill", "elevation": 2700, "province": "Koshi"},
    "Palpa": {"region": "Hill", "elevation": 2000, "province": "Lumbini"},
    "Panchthar": {"region": "Hill", "elevation": 2700, "province": "Koshi"},
    "Parasi": {"region": "Terai", "elevation": 400, "province": "Lumbini"},
    "Parbat": {"region": "Hill", "elevation": 2300, "province": "Gandaki"},
    "Parsa": {"region": "Terai", "elevation": 100, "province": "Madhesh"},
    "Pyuthan": {"region": "Hill", "elevation": 2500, "province": "Lumbini"},
    "Ramechhap": {"region": "Hill", "elevation": 2700, "province": "Bagmati"},
    "Rasuwa": {"region": "Mountain", "elevation": 2800, "province": "Bagmati"},
    "Rautahat": {"region": "Terai", "elevation": 100, "province": "Madhesh"},
    "Rolpa": {"region": "Hill", "elevation": 2500, "province": "Lumbini"},
    "Rupandehi": {"region": "Terai", "elevation": 100, "province": "Lumbini"},
    "Salyan": {"region": "Hill", "elevation": 2800, "province": "Karnali"},
    "Sankhuwasabha": {"region": "Hill", "elevation": 2700, "province": "Koshi"},
    "Saptari": {"region": "Terai", "elevation": 100, "province": "Madhesh"},
    "Sarlahi": {"region": "Terai", "elevation": 100, "province": "Madhesh"},
    "Sindhuli": {"region": "Hill", "elevation": 2200, "province": "Bagmati"},
    "Sindhupalchok": {"region": "Hill", "elevation": 2800, "province": "Bagmati"},
    "Siraha": {"region": "Terai", "elevation": 100, "province": "Madhesh"},
    "Solukhumbu": {"region": "Mountain", "elevation": 2700, "province": "Koshi"},
    "Sunsari": {"region": "Terai", "elevation": 100, "province": "Koshi"},
    "Surkhet": {"region": "Hill", "elevation": 600, "province": "Karnali"},
    "Syangja": {"region": "Hill", "elevation": 2000, "province": "Gandaki"},
    "Tanahun": {"region": "Hill", "elevation": 2000, "province": "Gandaki"},
    "Taplejung": {"region": "Mountain", "elevation": 2700, "province": "Koshi"},
    "Terhathum": {"region": "Hill", "elevation": 2700, "province": "Koshi"},
    "Udayapur": {"region": "Hill", "elevation": 1800, "province": "Koshi"},
    "West Rukum": {"region": "Hill", "elevation": 2600, "province": "Lumbini"}
}

# Add metadata to test_df
test_df['region'] = test_df['District'].map(lambda x: district_metadata.get(x, {}).get('region', 'Unknown'))
test_df['elevation'] = test_df['District'].map(lambda x: district_metadata.get(x, {}).get('elevation', 0))

# Regional analysis
print("\n" + "="*70)
print("🗺️  REGIONAL PERFORMANCE BREAKDOWN")
print("="*70)

regional_stats = test_df.groupby('region')['error'].agg(['count', 'mean', 'std']).round(4)
regional_stats.columns = ['Samples', 'MAE (°C)', 'Std Dev']
regional_stats = regional_stats.sort_values('MAE (°C)')

print(regional_stats.to_string())

# District-level analysis
print("\n" + "="*70)
print("📍 TOP 10 BEST PERFORMING DISTRICTS")
print("="*70)

district_stats = test_df.groupby('District')['error'].agg(['count', 'mean']).round(4)
district_stats.columns = ['Samples', 'MAE (°C)']
district_stats = district_stats[district_stats['Samples'] >= 10]  # Min 10 samples
top_10 = district_stats.nsmallest(10, 'MAE (°C)')

for i, (district, row) in enumerate(top_10.iterrows(), 1):
    meta = district_metadata.get(district, {})
    print(f"{i:2d}. {district:20s} - MAE: {row['MAE (°C)']:.4f}°C ({row['Samples']:4.0f} samples) [{meta.get('region', 'Unknown')}]")

print("\n" + "="*70)
print("📍 TOP 10 WORST PERFORMING DISTRICTS")
print("="*70)

bottom_10 = district_stats.nlargest(10, 'MAE (°C)')

for i, (district, row) in enumerate(bottom_10.iterrows(), 1):
    meta = district_metadata.get(district, {})
    print(f"{i:2d}. {district:20s} - MAE: {row['MAE (°C)']:.4f}°C ({row['Samples']:4.0f} samples) [{meta.get('region', 'Unknown')}]")

# Save results
print("\n" + "="*70)
print("💾 SAVING RESULTS")
print("="*70)

# Save detailed results
test_df.to_csv('analysis/regional_analysis_results.csv', index=False)
print("✅ Saved: analysis/regional_analysis_results.csv")

# Create summary for paper
summary = {
    'overall': {
        'mae': float(mae),
        'rmse': float(rmse),
        'r2': float(r2),
        'training_time': float(training_time),
        'train_samples': len(X_train),
        'test_samples': len(X_test)
    },
    'regional': regional_stats.to_dict(),
    'top_10_best': top_10.to_dict(),
    'bottom_10_worst': bottom_10.to_dict()
}

import json
with open('analysis/performance_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)
print("✅ Saved: analysis/performance_summary.json")

print("\n" + "="*70)
print("✅ ANALYSIS COMPLETE - ALL NUMBERS ARE REAL!")
print("="*70)
print("\nUse these results to update your paper's Results section.")
