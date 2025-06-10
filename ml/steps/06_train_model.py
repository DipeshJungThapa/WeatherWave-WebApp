# ml/steps/06_train_model.py
import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor # A common choice for regression
from sklearn.metrics import mean_absolute_error, r2_score

def train_weather_model(input_file="ml/data/encoded_districts.csv",
                        model_output_path="ml/models/weather_model.pkl",
                        target_column='Temp_2m_tomorrow',
                        test_size=0.2,
                        random_state=42):
    """
    Loads the preprocessed data, splits it into training and testing sets,
    trains a RandomForestRegressor model, evaluates it, and saves the trained model.

    Input: ml/data/encoded_districts.csv
    Output: ml/models/weather_model.pkl
    """
    print(f"--- Starting 06_train_model.py ---")
    print(f"Loading data from: {input_file}")

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        print("Please ensure 'encoded_districts.csv' is in the 'ml/data/' directory after running 05_encode_district.py.")
        return False

    print(f"Data loaded. Shape: {df.shape}")

    # Define features (X) and target (y)
    # We need to exclude non-feature columns like 'Date' and the original 'District'
    # The encoded 'District_encoded' should be included if it exists
    features = [col for col in df.columns if col not in ['Date', 'District', target_column]]

    if 'District_encoded' in df.columns and 'District' in features:
        features.remove('District') # Ensure original 'District' is not used as a feature if encoded exists

    X = df[features]
    y = df[target_column]

    print(f"Features (X) shape: {X.shape}")
    print(f"Target (y) shape: {y.shape}")
    print(f"Features used: {features}")


    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    print(f"Data split into training ({len(X_train)} samples) and testing ({len(X_test)} samples).")

    # Initialize and train the model
    print("Training RandomForestRegressor model...")
    model = RandomForestRegressor(n_estimators=100, random_state=random_state, n_jobs=-1) # n_jobs=-1 uses all available cores
    model.fit(X_train, y_train)
    print("Model training complete.")

    # Evaluate the model
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\nModel Evaluation:")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"R-squared (R2) Score: {r2:.2f}")

    # Ensure model output directory exists
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)

    # Save the trained model (will be ignored by Git due to .gitignore)
    joblib.dump(model, model_output_path)
    print(f"Trained model saved to: {model_output_path}")

    print(f"--- Finished 06_train_model.py ---")
    return True

if __name__ == "__main__":
    train_weather_model()