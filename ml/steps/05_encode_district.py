# ml/steps/05_encode_district.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib # For saving the encoder
import os

def encode_district(input_file="ml/data/no_missing.csv",
                    output_file="ml/data/encoded_districts.csv",
                    encoder_output_path="ml/models/label_encoder.pkl"):
    """
    Reads the data, encodes the 'District' column using LabelEncoder,
    and saves both the transformed data and the fitted encoder.

    Input: data/no_missing.csv
    Output: data/encoded_districts.csv
    Encoder Output: ml/models/label_encoder.pkl
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
    print("Initial columns:")
    print(df.columns.tolist())

    # Objective: Encode the 'District' column from text to numerical.
    if 'District' in df.columns:
        le = LabelEncoder()
        df['District_Encoded'] = le.fit_transform(df['District'])
        print(" 'District' column encoded to 'District_Encoded' successfully.")

        # Save the fitted LabelEncoder
        os.makedirs(os.path.dirname(encoder_output_path), exist_ok=True) # Ensure models directory exists
        joblib.dump(le, encoder_output_path)
        print(f"LabelEncoder saved to: {encoder_output_path}")

        # Drop the original 'District' column as it's now encoded
        df.drop('District', axis=1, inplace=True)
        print(" Original 'District' column dropped.")
    else:
        print("Error: 'District' column not found. Cannot encode.")
        return False

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save the data with encoded districts
    df.to_csv(output_file, index=False)
    print(f"Data with encoded districts saved to: {output_file}")
    print(f"Final shape: {df.shape}")
    print(f"Final columns (with encoded district):")
    print(df.columns.tolist())
    print(f"--- Finished 05_encode_district.py ---")
    return True

if __name__ == "__main__":
    encode_district()