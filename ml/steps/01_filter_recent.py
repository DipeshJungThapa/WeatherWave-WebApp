# ml/steps/01_filter_recent.py
import pandas as pd
import os

def filter_recent_data(input_file="ml/data/raw_climate_data.csv", output_file="ml/data/filtered.csv"):
    """
    Reads the raw climate data, filters it to 2017-2019, sorts it,
    and saves the filtered data.

    Args:
        input_file (str): Path to the raw CSV file.
        output_file (str): Path where the filtered CSV will be saved.
    """
    print(f"--- Starting 01_filter_recent.py ---")
    print(f"Loading raw data from: {input_file}")

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        print("Please ensure 'raw_climate_data.csv' is in the 'ml/data/' directory.")
        return False # Indicate failure

    print(f"Initial shape: {df.shape}")

    # Convert Date column to datetime format
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        print(" 'Date' column converted to datetime format.")
    else:
        print("Error: 'Date' column not found in the dataset. Exiting.")
        return False # Indicate failure


    # Objective: Keep only rows from January 1, 2017 to December 31, 2019.
    start_date = '2017-01-01'
    end_date = '2019-12-31'
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    print(f"Shape after filtering for dates between {start_date} and {end_date}: {df.shape}")

    # Sort data by District and Date
    # This is crucial for later steps like adding the 'Temp_2m_tomorrow' column
    if 'District' in df.columns and 'Date' in df.columns:
        df = df.sort_values(by=['District', 'Date']).reset_index(drop=True)
        print(" Data sorted by 'District' and 'Date'.")
    else:
        print("Warning: 'District' or 'Date' column not found for sorting. Proceeding without sorting.")


    # Ensure output directory exists (redundant after mkdir -p, but good for robustness)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save the filtered version
    df.to_csv(output_file, index=False)
    print(f"Filtered data saved to: {output_file}")
    print(f"Final shape: {df.shape}")
    print(f"--- Finished 01_filter_recent.py ---")
    return True # Indicate success

if __name__ == "__main__":
    filter_recent_data()