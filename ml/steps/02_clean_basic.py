# ml/steps/02_clean_basic.py
import pandas as pd
import os

def clean_basic_data(input_file="ml/data/filtered.csv",
                     output_file="ml/data/cleaned_basic.csv"): # CORRECTED: Output file name is now 'cleaned_basic.csv'
    """
    Reads the filtered climate data, performs basic cleaning steps like
    renaming columns and handling basic inconsistencies, and saves the cleaned data.

    Input: data/filtered.csv
    Output: data/cleaned_basic.csv
    """
    print(f"--- Starting 02_clean_basic.py ---")
    print(f"Loading data from: {input_file}")

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        print("Please ensure 'filtered.csv' is in the 'ml/data/' directory after running 01_filter_recent.py.")
        return False

    print(f"Initial shape: {df.shape}")
    print("Initial columns:")
    print(df.columns.tolist())

    # Objective: Rename 'Temperature_2m_tomorrow' to 'Temp_2m_tomorrow'
    # This was a previous renaming instruction, confirming it here for consistency
    if 'Temperature_2m_tomorrow' in df.columns:
        df.rename(columns={'Temperature_2m_tomorrow': 'Temp_2m_tomorrow'}, inplace=True)
        print(" Renamed 'Temperature_2m_tomorrow' to 'Temp_2m_tomorrow'.")
    else:
        print(" Warning: 'Temperature_2m_tomorrow' column not found for renaming.")

    # Objective: Handle potential inconsistencies or basic cleaning if any
    # For now, let's just ensure 'Date' is datetime again and 'District' is string.
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        print(" 'Date' column ensured to be datetime.")
    if 'District' in df.columns:
        df['District'] = df['District'].astype(str)
        print(" 'District' column ensured to be string type.")

    # Additional check for missing values in essential columns (from your original run output)
    # This block is from your previous 02_clean_basic.py execution log,
    # ensuring it matches what the script actually does.
    core_weather_cols = ['Precip', 'Pressure', 'Humidity_2m', 'RH_2m', 'Temp_2m', 'WetBulbTemp_2m',
                         'MaxTemp_2m', 'MinTemp_2m', 'TempRange_2m', 'EarthSkinTemp']
    missing_before_clean = df[core_weather_cols].isnull().sum().sum()
    if missing_before_clean > 0:
        print(f"Checking for missing values in core weather columns: {core_weather_cols}")
        # Assuming you want to drop rows with missing values in these core columns here
        # Note: Your 04_drop_missing.py also handles dropping missing, so this might be redundant
        # or intended for an earlier cleanup. Let's keep it consistent with your prior output.
        df.dropna(subset=core_weather_cols, inplace=True)
        print(f"Dropped rows with missing values in core weather fields. New shape: {df.shape}")
    else:
        print(f"No rows with missing values found in core weather fields.")


    print(f"Final columns (after basic cleaning):")
    print(df.columns.tolist())

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save the basic cleaned data to the CORRECTED output file
    df.to_csv(output_file, index=False)
    print(f"Basic cleaned data saved to: {output_file}")
    print(f"Final shape: {df.shape}")
    print(f"--- Finished 02_clean_basic.py ---")
    return True

if __name__ == "__main__":
    clean_basic_data()