# ml/steps/05_encode_district.py
import pandas as pd
import os
import joblib # For saving the LabelEncoder
from sklearn.preprocessing import LabelEncoder

def encode_district_column(input_file="ml/data/no_missing.csv",
                           output_file="ml/data/encoded_districts.csv",
                           encoder_path="ml/models/label_encoder.pkl",
                           column_to_encode='District'):
    """
    Reads the data, applies Label Encoding to the 'District' column,
    saves the fitted LabelEncoder, and saves the data with the encoded column.

    Input: data/no_missing.csv
    Output: data/encoded_districts.csv
    Saves: ml/models/label_encoder.pkl
    """
    print(f"--- Starting 05_encode_district.py ---")
    print(f"Loading data from: {input_file}")

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        print("Please ensure 'no_missing.csv' is in the 'ml/data/' directory after running 04_drop_missing.py.")
        return False

    print(f"Initial shape: {df.shape}")
    print(f"Unique values in '{column_to_encode}' before encoding: {df[column_to_encode].nunique()}")

    # Objective: Apply Label Encoding to the 'District' column
    if column_to_encode in df.columns:
        le = LabelEncoder()
        df[column_to_encode + '_encoded'] = le.fit_transform(df[column_to_encode])
        print(f" '{column_to_encode}' column encoded to '{column_to_encode}_encoded'.")
        print(f"Unique encoded values: {df[column_to_encode + '_encoded'].nunique()}")
    else:
        print(f"Error: Column '{column_to_encode}' not found for encoding.")
        return False

    # Ensure models directory exists for saving encoder
    os.makedirs(os.path.dirname(encoder_path), exist_ok=True)

    # Save the fitted LabelEncoder (this will be ignored by Git due to .gitignore)
    joblib.dump(le, encoder_path)
    print(f"Fitted LabelEncoder saved to: {encoder_path}")

    # Ensure output directory exists for saving data
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save the data with the new encoded column
    df.to_csv(output_file, index=False)
    print(f"Data with encoded districts saved to: {output_file}")
    print(f"Final shape: {df.shape}")
    print(f"Final columns (with encoded district):")
    print(df.columns.tolist())
    print(f"--- Finished 05_encode_district.py ---")
    return True

if __name__ == "__main__":
    encode_district_column()