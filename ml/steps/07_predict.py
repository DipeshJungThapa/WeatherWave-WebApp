import pandas as pd
import joblib
import os
import argparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # goes to root 'project/'

MODEL_PATH = os.path.join(BASE_DIR, 'models', 'weather_model.pkl')
LABEL_ENCODER_PATH = os.path.join(BASE_DIR, 'models', 'label_encoder.pkl')
DATA_PATH = os.path.join(BASE_DIR, 'data', 'encoded_districts.csv')
PREDICTIONS_OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'predictions.csv')

print("--- Starting 07_predict.py ---")

try:
    print(f"Loading model from: {MODEL_PATH}")
    loaded_model = joblib.load(MODEL_PATH)

    print(f"Loading label encoder from: {LABEL_ENCODER_PATH}")
    loaded_label_encoder = joblib.load(LABEL_ENCODER_PATH)

    print("Model and Label Encoder loaded successfully.")

    MODEL_FEATURES = [
        'Latitude', 'Longitude', 'Precip', 'Pressure', 'Humidity_2m', 'RH_2m',
        'Temp_2m', 'WetBulbTemp_2m', 'MaxTemp_2m', 'MinTemp_2m', 'EarthSkinTemp',
        'WindSpeed_10m', 'MaxWindSpeed_10m', 'MinWindSpeed_10m',
        'WindSpeed_50m', 'MaxWindSpeed_50m', 'MinWindSpeed_50m',
        'District_encoded'
    ]

    # Argument parsing (district argument is optional now)
    parser = argparse.ArgumentParser(description="Predict tomorrow's temperature using a trained ML model.")
    parser.add_argument('--district', type=str, help="Specific district name for single prediction (ignored in this version).")
    args = parser.parse_args()

    print(f"Loading data for prediction from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    df['Date'] = pd.to_datetime(df['Date'])
    print(f"Data shape for prediction: {df.shape}")

    # Make batch predictions for the entire dataset
    print("\nMaking batch predictions for the entire dataset...")
    X = df[MODEL_FEATURES]
    predictions = loaded_model.predict(X)

    df['predicted_Temp_2m_tomorrow'] = predictions
    df.to_csv(PREDICTIONS_OUTPUT_PATH, index=False)
    print(f"Predictions saved to: {PREDICTIONS_OUTPUT_PATH}")
    print(f"Final data shape with predictions: {df.shape}")

    # Now show the latest Kathmandu data only on terminal output
    # Kathmandu encoded value is 35
    kathmandu_encoded_val = 35
    kathmandu_rows = df[df['District_encoded'] == kathmandu_encoded_val]
    if kathmandu_rows.empty:
        print("Warning: No data found for Kathmandu (encoded=35). Cannot show latest prediction.")
    else:
        latest_date = kathmandu_rows['Date'].max()
        latest_kathmandu_data = kathmandu_rows[kathmandu_rows['Date'] == latest_date]

        print("\n--- Latest Kathmandu Prediction ---")
        display_cols = ['Date', 'District', 'Temp_2m_tomorrow', 'predicted_Temp_2m_tomorrow']
        # 'District' column is assumed to exist; if not, can be dropped or handled differently
        if 'District' not in latest_kathmandu_data.columns:
            display_cols.remove('District')
        print(latest_kathmandu_data[display_cols].to_string(index=False))
        print("--- End of Kathmandu Prediction ---")

except FileNotFoundError as e:
    print(f"Error: Required file not found - {e}")
    print("Please run steps 01-06 of your ML pipeline first to generate these files.")
except KeyError as e:
    print(f"Error: Missing expected column in data - {e}")
    print("Check if data structure matches model expectation and MODEL_FEATURES list.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("--- Finished 07_predict.py ---")
