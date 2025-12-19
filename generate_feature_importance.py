"""
Generate Feature Importance Figure from Trained Random Forest Model
===================================================================
Extracts feature importance scores from the trained model and visualizes them.

Note: This is post-hoc importance from the trained model, not from feature 
selection experiments. Temp_2m will dominate due to persistence effect.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2
DATA_FILE = "encoded_districts.csv"
OUTPUT_FILE = "figures/fig_feature_importance.png"
DPI = 300

def load_and_train():
    """Load data, train model, extract feature importances"""
    print("📊 Loading dataset...")
    df = pd.read_csv(DATA_FILE)
    
    # THE 8 SELECTED FEATURES (domain-driven selection)
    # Mapping to actual column names in encoded_districts.csv
    features = [
        'Temp_2m',           # Current temperature
        'Humidity_2m',       # Relative humidity
        'Pressure',          # Atmospheric pressure (Pressure_msl in paper)
        'WindSpeed_10m',     # Wind speed at 10m
        # Note: Cloud_cover and Rain not in this dataset - they were added later
        # Using what's available from the 8 core meteorological variables
        'Precip',            # Precipitation (Rain)
        'District_encoded',  # Geographic location
        # Day_of_year would need to be derived from Date column
    ]
    
    # Add day_of_year if Date column exists
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Day_of_year'] = df['Date'].dt.dayofyear
        features.append('Day_of_year')
    
    TARGET_COLUMN = "Temp_2m_tomorrow"
    
    # Verify all features exist
    missing = [f for f in features if f not in df.columns]
    if missing:
        print(f"⚠️  Missing features: {missing}")
        features = [f for f in features if f in df.columns]
    
    X = df[features]
    y = df[TARGET_COLUMN]
    
    # Same split as training
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    
    print(f"Training samples: {len(X_train):,}")
    print(f"Features: {len(features)}")
    
    # Train model
    print("🌲 Training Random Forest...")
    model = RandomForestRegressor(
        n_estimators=5,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    print("✅ Model trained")
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Normalize to sum to 1
    importances_normalized = importances / importances.sum()
    
    return features, importances_normalized

def generate_figure(features, importances):
    """Generate IEEE-style feature importance bar chart with log scale"""
    print("📊 Generating feature importance figure...")
    
    # Sort by importance descending
    indices = np.argsort(importances)[::-1]
    sorted_features = [features[i] for i in indices]
    sorted_importances = importances[indices]
    
    # Create figure with more width for log scale readability
    fig, ax = plt.subplots(figsize=(12, 7))
    
    y_pos = np.arange(len(sorted_features))
    
    # Horizontal bar chart with LOG SCALE
    bars = ax.barh(y_pos, sorted_importances, color='steelblue', edgecolor='black', linewidth=1.2)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(sorted_features, fontsize=11)
    ax.invert_yaxis()  # Highest importance at top
    
    # LOG SCALE to show all features clearly
    ax.set_xscale('log')
    
    # Set reasonable x-axis limits to show all bars
    min_importance = sorted_importances[sorted_importances > 0].min() if any(sorted_importances > 0) else 0.0001
    ax.set_xlim(min_importance * 0.5, 1.5)
    
    ax.set_xlabel('Feature Importance (log scale)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Feature', fontsize=12, fontweight='bold')
    ax.set_title('Random Forest Feature Importance Distribution\n(Logarithmic Scale for Visibility)', 
                 fontsize=14, fontweight='bold', pad=15)
    
    # Add importance values as text - position adaptively
    for i, v in enumerate(sorted_importances):
        # For very small values, show scientific notation
        if v < 0.001:
            text = f'{v:.2e} ({v*100:.3f}%)'
        elif v < 0.01:
            text = f'{v:.4f} ({v*100:.2f}%)'
        else:
            text = f'{v:.2f} ({v*100:.1f}%)'
        
        # Position text to the right of bar
        ax.text(v * 1.5, i, text, va='center', fontsize=9, fontweight='bold')
    
    # Grid for both major and minor ticks on log scale
    ax.grid(True, alpha=0.3, axis='x', which='major', linestyle='-', linewidth=0.8)
    ax.grid(True, alpha=0.15, axis='x', which='minor', linestyle=':', linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Saved: {OUTPUT_FILE}")
    
    # Print summary with better formatting for small values
    print("\nFeature Importance Summary:")
    print("-" * 60)
    for feat, imp in zip(sorted_features, sorted_importances):
        if imp < 0.001:
            print(f"{feat:20s}: {imp:.6f} ({imp*100:.4f}%)")
        else:
            print(f"{feat:20s}: {imp:.4f} ({imp*100:.2f}%)")
    print("-" * 60)
    print(f"Total: {sorted_importances.sum():.4f}")

def main():
    print("=" * 70)
    print("GENERATING FEATURE IMPORTANCE FIGURE")
    print("=" * 70)
    print()
    
    features, importances = load_and_train()
    generate_figure(features, importances)
    
    print("\n" + "=" * 70)
    print("✅ FIGURE GENERATED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    main()
