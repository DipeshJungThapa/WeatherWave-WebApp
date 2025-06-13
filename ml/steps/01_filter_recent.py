# ml/steps/01_filter_recent.py
import pandas as pd
import os

def filter_recent_data(input_file="ml/data/raw_climate_data.csv",
                       output_file="ml/data/filtered.csv",
                       recent_years=10):
    """
    Reads the raw climate data, filters it to include only the most recent years,
    and saves the filtered data.

    Input: data/raw_climate_data.csv
    Output: data/filtered.csv
    """
    print(f"--- Starting 01_filter_recent.py ---")
    print(f"Loading data from: {input_file}")

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        print("Please ensure 'raw_climate_data.csv' is in the 'ml/data/' directory.")
        return False

    print(f"Initial shape: {df.shape}")

    # Ensure 'Date' column is in datetime format
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        print(" 'Date' column converted to datetime.")
    else:
        print("Error: 'Date' column not found. Cannot filter by date.")
        return False

    # Filter for the most recent years
    current_year = df['Date'].dt.year.max() # Get the latest year in the dataset
    start_year = current_year - recent_years + 1 # Calculate the start year for filtering

    df_filtered = df[df['Date'].dt.year >= start_year]
    print(f"Filtered data for years {start_year} to {current_year}.")
    print(f"Filtered shape: {df_filtered.shape}")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save the filtered data
    df_filtered.to_csv(output_file, index=False)
    print(f"Filtered data saved to: {output_file}")
    print(f"--- Finished 01_filter_recent.py ---")
    return True

if __name__ == "__main__":
    filter_recent_data()