# ml/steps/07_predict.py
import pandas as pd
import os
import joblib

def predict_weather(model_path="ml/models/weather_model.pkl",
                    encoder_path="ml/models/label_encoder.pkl",
                    sample_data_path="ml/data/encoded_districts.csv", # Using existing data for demonstration
                    num_samples=5):
    """
    Loads the trained model and label encoder, prepares sample data for prediction,
    and makes predictions.

    Inputs:
        ml/models/weather_model.pkl (trained model)
        ml/models/label_encoder.pkl (fitted label encoder for 'District')
        ml/data/encoded_districts.csv (source for sample data to predict on)
    """
    print(f"--- Starting 07_predict.py ---")
    print(f"Loading trained model from: {model_path}")

    try:
        model = joblib.load(model_path)
        print("Model loaded successfully.")
    except FileNotFoundError:
        print(f"Error: The model file '{model_path}' was not found.")
        print("Please ensure 'weather_model.pkl' is in the 'ml/models/' directory after running 06_train_model.py.")
        return False

    print(f"Loading label encoder from: {encoder_path}")
    try:
        le = joblib.load(encoder_path)
        print("Label Encoder loaded successfully.")
    except FileNotFoundError:
        print(f"Error: The label encoder file '{encoder_path}' was not found.")
        print("Please ensure 'label_encoder.pkl' is in the 'ml/models/' directory after running 05_encode_district.py.")
        return False

    print(f"Loading sample data from: {sample_data_path}")
    try:
        # Load the entire preprocessed dataset (as it's already encoded)
        df_encoded = pd.read_csv(sample_data_path)
    except FileNotFoundError:
        print(f"Error: The sample data file '{sample_data_path}' was not found.")
        print("Please ensure 'encoded_districts.csv' is in the 'ml/data/' directory.")
        return False

    # Take a small random sample from the test set (or any part of the data)
    # We need to select the same features used for training (excluding target and original 'Date', 'District')
    target_column = 'Temp_2m_tomorrow'
    features = [col for col in df_encoded.columns if col not in ['Date', 'District', target_column]]

    # If 'District_encoded' is present and 'District' was accidentally kept in features, remove it
    if 'District_encoded' in df_encoded.columns and 'District' in features:
        features.remove('District')

    sample_for_prediction = df_encoded[features].sample(n=num_samples, random_state=42)
    original_target_values = df_encoded.loc[sample_for_prediction.index, target_column]
    print(f"\n--- Sample Data for Prediction ({num_samples} samples) ---")
    print(sample_for_prediction)

    # Make predictions
    print("\nMaking predictions...")
    predictions = model.predict(sample_for_prediction)

    print("\n--- Predictions ---")
    for i, pred in enumerate(predictions):
        original_temp = original_target_values.iloc[i] if not pd.isna(original_target_values.iloc[i]) else 'N/A'
        print(f"Sample {i+1}: Predicted Temp_2m_tomorrow = {pred:.2f}°C (Actual: {original_temp}°C)")

    # Example of predicting for a *new* single data point (manually constructed)
    print("\n--- Example: Predicting for a single new, hypothetical data point ---")
    # This requires knowing the feature order and meaning.
    # For a real web app, you'd get this data from user input or an API.
    # Example: Let's assume a hypothetical data point, ensuring 'District_Encoded' is handled.
    # For a real scenario, you'd get raw input and pass it through all preprocessing steps first.

    # Example of how to encode a new district for prediction if needed
    # new_district_name = "Kathmandu"
    # try:
    #     encoded_new_district = le.transform([new_district_name])[0]
    #     print(f"'{new_district_name}' encoded as: {encoded_new_district}")
    # except ValueError:
    #     print(f"Warning: '{new_district_name}' not seen during training, cannot encode.")
    #     encoded_new_district = -1 # Or handle appropriately

    # For demonstration, we'll use the first row of our sample for its feature values,
    # then modify it slightly to show a prediction on a constructed point.
    first_sample_row = sample_for_prediction.iloc[0:1] # Get first sample as a DataFrame
    # hypot_temp_2m = 25.0
    # first_sample_row['Temp_2m'] = hypot_temp_2m # Modify a feature to see effect (ensure column exists)

    hypothetical_prediction = model.predict(first_sample_row)
    print(f"Hypothetical prediction for a sample: {hypothetical_prediction[0]:.2f}°C")


    print(f"--- Finished 07_predict.py ---")
    return True

if __name__ == "__main__":
    predict_weather()