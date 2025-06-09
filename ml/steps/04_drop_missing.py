# ml/steps/04_drop_missing.py
import pandas as pd
import os

def drop_missing_values(input_file="ml/data/with_target.csv", output_file="ml/data/no_missing.csv"):
    """
    Reads the data with the target column, drops rows with missing values
    in essential features or the target, and saves the cleaned data.

    Input: data/with_target.csv
    Output: data/no_missing.csv
    """
    print(f"--- Starting 04_drop_missing.py ---")
    print(f"Loading data from: {input_file}")

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        print("Please ensure 'with_target.csv' is in the 'ml/data/' directory after running 03_add_target_column.py.")
        return False

    print(f"Initial shape: {df.shape}")

    # Define the columns that MUST NOT have missing values for model training
    # This includes the target and key input features.
    # Based on your data, we'll select relevant weather features and the target.
    # Note: 'Unnamed: 0' and 'Latitude', 'Longitude' are not critical for model training directly,
    # so we focus on the weather features and the target.
    essential_columns = [
        'Precip', 'Pressure', 'Humidity_2m', 'RH_2m', 'Temp_2m',
        'WetBulbTemp_2m', 'MaxTemp_2m', 'MinTemp_2m', 'TempRange_2m',
        'EarthSkinTemp', 'WindSpeed_10m', 'MaxWindSpeed_10m',
        'MinWindSpeed_10m', 'WindSpeedRange_10m', 'WindSpeed_50m',
        'MaxWindSpeed_50m', 'MinWindSpeed_50m', 'WindSpeedRange_50m',
        'Temp_2m_tomorrow' # The target column - CRITICAL!
    ]

    # Filter to only existing essential columns
    existing_essential_columns = [col for col in essential_columns if col in df.columns]

    print(f"Checking for missing values in essential columns: {existing_essential_columns}")
    initial_rows = df.shape[0]

    # Objective: Drop rows where any of your chosen weather columns
    # or Temp_2m_tomorrow is blank (the label is missing).
    df.dropna(subset=existing_essential_columns, inplace=True)
    rows_dropped = initial_rows - df.shape[0]

    if rows_dropped > 0:
        print(f"Dropped {rows_dropped} rows with missing values in essential features or target.")
    else:
        print("No rows with missing values found in essential features or target.")

    # Verify no missing values left in essential columns
    missing_counts = df[existing_essential_columns].isnull().sum()
    if missing_counts.sum() == 0:
        print("Successfully removed all missing values from essential columns.")
    else:
        print("Warning: Missing values still present in some essential columns after dropna.")
        print(missing_counts[missing_counts > 0])


    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save the data with no missing values
    df.to_csv(output_file, index=False)
    print(f"Cleaned data (no missing values) saved to: {output_file}")
    print(f"Final shape: {df.shape}")
    print(f"--- Finished 04_drop_missing.py ---")
    return True

if __name__ == "__main__":
    drop_missing_values()