# ml/steps/03_add_target_column.py
import pandas as pd
import os

def add_target_column(input_file="ml/data/cleaned_basic.csv", # Input file now reflects 'cleaned_basic.csv'
                      output_file="ml/data/with_target.csv",
                      target_column='Temp_2m_tomorrow'):
    """
    Reads the cleaned data, ensures the target column exists, and saves the data.
    This step is primarily for verification that the target column is present
    and correctly named after earlier cleaning steps.

    Input: data/cleaned_basic.csv
    Output: data/with_target.csv
    """
    print(f"--- Starting 03_add_target_column.py ---")  
    print(f"Loading data from: {input_file}")

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        print("Please ensure 'cleaned_basic.csv' is in the 'ml/data/' directory after running 02_clean_basic.py.")
        return False

    print(f"Initial shape: {df.shape}")
    print("Initial columns:")
    print(df.columns.tolist())

    # Objective: Verify the presence of the target column
    if target_column in df.columns:
        print(f" Target column '{target_column}' is present.")
    else:
        print(f"Error: Target column '{target_column}' not found in the dataset.")
        print("Please ensure the column exists or adjust the target column name.")
        return False

    # No transformation needed in this step, just verification and saving
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save the data
    df.to_csv(output_file, index=False)
    print(f"Data with target column verified and saved to: {output_file}")
    print(f"Final shape: {df.shape}")
    print(f"--- Finished 03_add_target_column.py ---")
    return True

if __name__ == "__main__":
    add_target_column()