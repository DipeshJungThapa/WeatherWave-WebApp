# ml/steps/02_clean_basic.py
import pandas as pd
import os

def clean_basic_data(input_file="ml/data/filtered.csv",
                     output_file="ml/data/cleaned_basic.csv"): # Note: Output file name changed from 'no_missing.csv' to 'cleaned_basic.csv' to better reflect content
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

    print(f"Final columns (after basic cleaning):")
    print(df.columns.tolist())

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save the basic cleaned data
    df.to_csv(output_file, index=False)
    print(f"Basic cleaned data saved to: {output_file}")
    print(f"Final shape: {df.shape}")
    print(f"--- Finished 02_clean_basic.py ---")
    return True

if __name__ == "__main__":
    clean_basic_data()