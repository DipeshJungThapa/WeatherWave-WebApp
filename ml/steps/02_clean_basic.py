import pandas as pd
import os

input_file = 'ml/data/filtered.csv'
output_file = 'ml/data/cleaned_basic.csv'

print("--- Starting 02_clean_basic.py ---")

try:
    df = pd.read_csv(input_file)
    print(f"Loading data from: {input_file}")
    print(f"Initial shape: {df.shape}")
    print("Initial columns:")
    print(df.columns.tolist())

    # Example: Rename 'Temperature_2m_tomorrow' to 'Temp_2m_tomorrow' if it exists.
    # Based on your previous output, this warning might be expected if the column
    # isn't present in filtered.csv yet, which is fine as it's created later.
    if 'Temperature_2m_tomorrow' in df.columns:
        df.rename(columns={'Temperature_2m_tomorrow': 'Temp_2m_tomorrow'}, inplace=True)
        print("Renamed 'Temperature_2m_tomorrow' to 'Temp_2m_tomorrow'.")
    else:
        print("Warning: 'Temperature_2m_tomorrow' column not found for renaming.")

    # Ensure 'Date' column is datetime
    df['Date'] = pd.to_datetime(df['Date'])
    print("'Date' column ensured to be datetime.")

    # Ensure 'District' column is string type
    df['District'] = df['District'].astype(str)
    print("'District' column ensured to be string type.")

    print("Final columns (after basic cleaning):")
    print(df.columns.tolist())

    df.to_csv(output_file, index=False)
    print(f"Basic cleaned data saved to: {output_file}")
    print(f"Final shape: {df.shape}")

except FileNotFoundError:
    print(f"Error: The file '{input_file}' was not found. Please ensure filtered.csv is in the ml/data/ directory.")
except KeyError as e:
    print(f"Error: Required column not found - {e}. Please check the input CSV file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("--- Finished 02_clean_basic.py ---")