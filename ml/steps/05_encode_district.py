import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder
import joblib # <<< Make sure joblib is imported for saving the encoder

input_file = 'ml/data/no_missing.csv'
output_file = 'ml/data/encoded_districts.csv'
output_encoder_file = 'ml/models/label_encoder.pkl' # <<< Define path for saving the encoder

print("--- Starting 05_encode_district.py ---")

try:
    df = pd.read_csv(input_file)
    print(f"Loading data from: {input_file}")
    print(f"Initial shape: {df.shape}")

    # Initialize LabelEncoder
    le = LabelEncoder()

    # Apply Label Encoding to the 'District' column
    df['District_encoded'] = le.fit_transform(df['District'])

    print(f"Encoded 'District' column to 'District_encoded'.")
    print(f"Unique encoded districts: {df['District_encoded'].nunique()}")

    df.to_csv(output_file, index=False)
    print(f"Data with encoded districts saved to: {output_file}")
    print(f"Final shape: {df.shape}")

    # --- NEW ADDITION: Save the LabelEncoder object ---
    os.makedirs(os.path.dirname(output_encoder_file), exist_ok=True) # Ensure directory exists
    joblib.dump(le, output_encoder_file)
    print(f"Label encoder saved to: {output_encoder_file}")
    # --- END NEW ADDITION ---

except FileNotFoundError:
    print(f"Error: The file '{input_file}' was not found. Please ensure no_missing.csv is in the ml/data/ directory.")
except KeyError as e:
    print(f"Error: Required column not found - {e}. Please check the input CSV file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("--- Finished 05_encode_district.py ---")