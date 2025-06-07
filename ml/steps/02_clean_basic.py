# ml/steps/02_clean_basic.py
import pandas as pd
import os

def clean_basic_data(input_file="ml/data/filtered.csv", output_file="ml/data/with_target.csv"):
    """
    Reads the filtered climate data, performs basic cleaning, and saves the cleaned data.
    Input: data/filtered.csv
    Output: data/with_target.csv (passes through without target, to be updated next)
    """
    print(f"--- Starting 02_clean_basic.py ---")
    print(f"Loading data from: {input_file}")

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        print("Please ensure 'filtered.csv' is in the 'ml/data/' directory after running 01_filter_recent.py.")
        return False # Indicate failure

    print(f"Initial shape: {df.shape}")
    print("Initial columns:")
    print(df.columns.tolist())

    # Objective: Ensure the Date column is in proper date format.
    # This might be redundant if 01_filter_recent.py already converted it
    # and saved correctly, but it's good for robustness.
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        print(" 'Date' column ensured to be in datetime format.")
    else:
        print("Warning: 'Date' column not found. Skipping date format conversion.")

    # Objective: Drop any rows where all weather fields are blank or obviously invalid.
    # We will identify the weather-related columns based on your provided schema.
    # Assuming Latitude, Longitude, Date, District are NOT weather fields for this purpose.
    # We'll drop rows where values in these specific columns are NaN/blank.
    # Let's define the core weather columns based on your previous screenshot:
    weather_columns = [
        'Precip', 'Pressure', 'Humidity_2m', 'RH_2m', 'Temp_2m',
        'WetBulbTemp_2m', 'MaxTemp_2m', 'MinTemp_2m', 'TempRange_2m',
        'EarthSkinTemp', 'WindSpeed_2m', 'MaxWindSpeed_2m',
        'MinWindSpeed_2m', 'WindSpeed_5m', 'MaxWindSpeed_5m',
        'MinWindSpeed_5m', 'WindSpeed_Range_5m'
    ]

    # Check which of these weather columns actually exist in the DataFrame
    existing_weather_columns = [col for col in weather_columns if col in df.columns]
    print(f"Checking for missing values in core weather columns: {existing_weather_columns}")

    initial_rows = df.shape[0]
    # Drop rows where ANY of the specified weather_columns have NaN values
    df.dropna(subset=existing_weather_columns, inplace=True)
    rows_dropped = initial_rows - df.shape[0]

    if rows_dropped > 0:
        print(f"Dropped {rows_dropped} rows with missing values in core weather fields.")
    else:
        print("No rows with missing values found in core weather fields.")

    # Ensure output directory exists (redundant if already created, but safe)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save the cleaned version. Output is 'with_target.csv' as per plan.
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to: {output_file}")
    print(f"Final shape: {df.shape}")
    print(f"--- Finished 02_clean_basic.py ---")
    return True # Indicate success

if __name__ == "__main__":
    clean_basic_data()