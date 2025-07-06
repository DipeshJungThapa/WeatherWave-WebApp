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

    # Argument parsing
    parser = argparse.ArgumentParser(description="Predict tomorrow's temperature using a trained ML model.")
    parser.add_argument('--district', type=str, help="Specific district name for single prediction.")
    args = parser.parse_args()

    print(f"Loading data for prediction from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    df['Date'] = pd.to_datetime(df['Date'])
    print(f"Data shape for prediction: {df.shape}")

    if args.district:
        district_name_input = args.district

        if district_name_input not in loaded_label_encoder.classes_:
            print(f"Error: District '{district_name_input}' not found in the trained model's known districts.")
            print(f"Known districts are: {', '.join(loaded_label_encoder.classes_)}")
            print("--- Finished 07_predict.py (with error) ---")
            exit(1)

        print(f"\nPreparing input features for '{district_name_input}' from historical data...")
        district_data = df[df['District'] == district_name_input].copy()

        if district_data.empty:
            print(f"Error: No historical data found for district '{district_name_input}'.")
            print("--- Finished 07_predict.py (with error) ---")
            exit(1)

        most_recent_data_row = district_data.sort_values(by='Date', ascending=True).iloc[-1]
        X_predict_single_row = pd.DataFrame([most_recent_data_row[MODEL_FEATURES]])

        print("\nFeatures prepared for prediction:")
        print(X_predict_single_row)

        print(f"\nMaking prediction for tomorrow's temperature in {district_name_input}...")
        predicted_temp = loaded_model.predict(X_predict_single_row)[0]

        print("\n-------------------------------------------")
        print(f"Predicted Temp_2m_tomorrow for {district_name_input}: {predicted_temp:.2f}°C")
        print("-------------------------------------------")

    else:
        print("\nMaking batch predictions for the entire dataset...")
        X = df[MODEL_FEATURES]
        predictions = loaded_model.predict(X)

        df['predicted_Temp_2m_tomorrow'] = predictions
        df.to_csv(PREDICTIONS_OUTPUT_PATH, index=False)
        print(f"Predictions saved to: {PREDICTIONS_OUTPUT_PATH}")
        print(f"Final data shape with predictions: {df.shape}")

        print("\n--- Spot-Checking 10 Random Sample Predictions vs. Actuals ---")
        if 'Temp_2m_tomorrow' in df.columns:
            sample_df = df.sample(n=10, random_state=42)[['Date', 'District', 'Temp_2m_tomorrow', 'predicted_Temp_2m_tomorrow']]
            print(sample_df)
        else:
            print("Note: 'Temp_2m_tomorrow' column not found for spot-checking.")
        print("--- Spot-Check Finished ---")

except FileNotFoundError as e:
    print(f"Error: Required file not found - {e}")
    print("Please run steps 01-06 of your ML pipeline first to generate these files.")
except KeyError as e:
    print(f"Error: Missing expected column in data - {e}")
    print("Check if data structure matches model expectation and MODEL_FEATURES list.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("--- Finished 07_predict.py ---")
