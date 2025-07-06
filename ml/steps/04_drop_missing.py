import pandas as pd
import os

input_file = 'ml/data/with_target.csv'
output_file = 'ml/data/no_missing.csv'

print("--- Starting 04_drop_missing.py ---")

try:
    df = pd.read_csv(input_file)
    print(f"Loading data from: {input_file}")
    print(f"Initial shape: {df.shape}")

    # Drop rows with any missing values (NaNs)
    initial_rows = df.shape[0]
    df.dropna(inplace=True)
    rows_dropped = initial_rows - df.shape[0]

    print(f"Dropped {rows_dropped} rows with missing values.")
    print(f"Final shape after dropping missing: {df.shape}")

    df.to_csv(output_file, index=False)
    print(f"Data with no missing values saved to: {output_file}")

except FileNotFoundError:
    print(f"Error: The file '{input_file}' was not found. Please ensure 'with_target.csv' is in the 'ml/data/' directory after running 03_add_target_column.py.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("--- Finished 04_drop_missing.py ---")