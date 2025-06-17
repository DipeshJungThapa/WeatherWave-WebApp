import pandas as pd
import os
import joblib # for loading models

input_data_file = 'ml/data/encoded_districts.csv' # Input data for prediction
input_model_file = 'ml/models/weather_model.pkl' # Correctly points to weather_model.pkl
output_prediction_file = 'ml/data/predictions.csv' # Example output file

print("--- Starting 07_predict.py ---")

try:
    # Load the trained model
    print(f"Loading model from: {input_model_file}")
    model = joblib.load(input_model_file)
    print("Model loaded successfully.")

    # Load data for prediction
    df_predict = pd.read_csv(input_data_file)
    print(f"Loading data for prediction from: {input_data_file}")
    print(f"Data shape for prediction: {df_predict.shape}")

    # Define the same features used during training in 06_train_model.py
    # This list explicitly excludes 'Unnamed: 0' and includes 'District_encoded'
    features = [
        'Latitude', 'Longitude', 'Precip', 'Pressure', 'Humidity_2m', 'RH_2m',
        'Temp_2m', 'WetBulbTemp_2m', 'MaxTemp_2m', 'MinTemp_2m', 'TempRange_2m',
        'EarthSkinTemp', 'WindSpeed_10m', 'MaxWindSpeed_10m', 'MinWindSpeed_10m',
        'WindSpeedRange_10m', 'WindSpeed_50m', 'MaxWindSpeed_50m',
        'MinWindSpeed_50m', 'WindSpeedRange_50m', 'District_encoded'
    ]

    # Check if all required features exist in the prediction data
    for col in features:
        if col not in df_predict.columns:
            raise KeyError(f"Missing required feature for prediction: {col}")

    X_predict = df_predict[features]

    # Make predictions
    print("Making predictions...")
    predictions = model.predict(X_predict)
    print("Predictions complete.")

    # Add predictions to the DataFrame
    df_predict['predicted_Temp_2m_tomorrow'] = predictions

    # Save predictions to a new CSV file
    df_predict.to_csv(output_prediction_file, index=False)
    print(f"Predictions saved to: {output_prediction_file}")
    print(f"Final data shape with predictions: {df_predict.shape}")

    # --- NEW ADDITION: Spot-check predictions ---
    print("\n--- Spot-Checking 10 Random Sample Predictions vs. Actuals ---")
    if 'Temp_2m_tomorrow' in df_predict.columns: # Ensure actual target column exists
        # Select 10 random rows for display
        random_samples = df_predict.sample(n=10, random_state=42) # random_state for reproducibility

        display_cols = ['Date', 'District', 'Temp_2m_tomorrow', 'predicted_Temp_2m_tomorrow']
        # Based on your pipeline, 'Date' and 'District' should be present in df_predict.

        print(random_samples[display_cols].to_string())
    else:
        print("Cannot perform spot-check: 'Temp_2m_tomorrow' (actuals) column not found in prediction data.")
    print("--- Spot-Check Finished ---")
    # --- END NEW ADDITION ---

except FileNotFoundError as e:
    print(f"Error: Required file not found - {e}. Ensure the model file and input data files exist.")
except KeyError as e:
    print(f"Error: A column required for prediction is missing - {e}. Please check your feature definitions or input data.")
except Exception as e:
    print(f"An unexpected error occurred during prediction: {e}")

print("--- Finished 07_predict.py ---")