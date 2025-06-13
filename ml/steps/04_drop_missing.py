# ml/steps/04_drop_missing.py
import pandas as pd
import os

def drop_missing_values(input_file="ml/data/with_target.csv",
                        output_file="ml/data/no_missing.csv", # Renamed back to no_missing.csv to reflect the result of this step
                        subset_columns=['Temp_2m', 'Precipitation', 'Wind_Speed', 'Temp_2m_tomorrow']):
    """
    Reads the data, drops rows with missing values in specified columns,
    and saves the data without missing values.

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
    print(f"Number of missing values before dropping:\n{df[subset_columns].isnull().sum()}")

    # Objective: Drop rows with missing values in the specified subset of columns
    df_no_missing = df.dropna(subset=subset_columns)
    print(f" Dropped rows with missing values in {subset_columns}.")

    print(f"Shape after dropping missing values: {df_no_missing.shape}")
    print(f"Number of missing values after dropping:\n{df_no_missing[subset_columns].isnull().sum()}")


    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save the data without missing values
    df_no_missing.to_csv(output_file, index=False)
    print(f"Data without missing values saved to: {output_file}")
    print(f"--- Finished 04_drop_missing.py ---")
    return True

if __name__ == "__main__":
    drop_missing_values()