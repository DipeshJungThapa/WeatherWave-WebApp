import pandas as pd
import os

input_file = 'ml/data/cleaned_basic.csv'
output_file = 'ml/data/with_target.csv'

print("--- Starting 03_add_target_column.py ---")

try:
    df = pd.read_csv(input_file)
    print(f"Loading data from: {input_file}")
    print(f"Initial shape: {df.shape}")
    print("Initial columns:")
    print(df.columns.tolist())

    # --- FIX FOR 'Temp_2m_tomorrow' NOT FOUND ERROR ---
    # Ensure 'Date' is datetime for correct sorting and shifting
    df['Date'] = pd.to_datetime(df['Date'])

    # Sort data by District and then Date to correctly align next-day values
    df = df.sort_values(by=['District', 'Date']).reset_index(drop=True)

    # Create the 'Temp_2m_tomorrow' target column using shift(-1)
    # This gets the temperature from the next row within each district group.
    df['Temp_2m_tomorrow'] = df.groupby('District')['Temp_2m'].shift(-1)
    # --- END FIX ---

    # Drop rows where Temp_2m_tomorrow is NaN (typically the last day for each district)
    initial_rows = df.shape[0]
    df.dropna(subset=['Temp_2m_tomorrow'], inplace=True)
    rows_dropped = initial_rows - df.shape[0]
    if rows_dropped > 0:
        print(f"Dropped {rows_dropped} rows due to missing 'Temp_2m_tomorrow' values (end of district data).")

    print(f"Columns after adding target: {df.columns.tolist()}")
    print(f"Final shape after adding target: {df.shape}")

    df.to_csv(output_file, index=False)
    print(f"Data with target column saved to: {output_file}")

except FileNotFoundError:
    print(f"Error: The file '{input_file}' was not found. Please ensure cleaned_basic.csv is in the ml/data/ directory.")
except KeyError as e:
    print(f"Error: Required column '{e}' not found for target creation. Please check the input CSV and column names.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("--- Finished 03_add_target_column.py ---")