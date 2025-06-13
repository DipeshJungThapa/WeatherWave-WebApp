# ml/steps/03_add_target_column.py
import pandas as pd
import os

def add_target_column(input_file="ml/data/with_target.csv", output_file="ml/data/with_target.csv"):
    """
    Adds the 'Temp_2m_tomorrow' target column to the dataset.
    Input: data/with_target.csv
    Output: data/with_target.csv (overwrites the input with the added column)
    """
    print(f"--- Starting 03_add_target_column.py ---")  
    print(f"Loading data from: {input_file}")

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        print("Please ensure 'with_target.csv' is in the 'ml/data/' directory after running 02_clean_basic.py.")
        return False # Indicate failure

    print(f"Initial shape: {df.shape}")
    print("Initial columns (before target column):")
    print(df.columns.tolist())

    # Ensure 'Date' column is datetime and 'District' exists for sorting
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    else:
        print("Error: 'Date' column not found. Cannot add target column without date information.")
        return False

    if 'District' not in df.columns:
        print("Error: 'District' column not found. Cannot add target column without district information.")
        return False

    # Objective: Sort by District and Date for correct shifting
    # This was done in 01_filter_recent, but re-sorting here for robustness
    # in case the file was somehow unsorted between steps.
    df = df.sort_values(by=['District', 'Date'])

    # Objective: For each district, add a new column that contains the temperature of the next day
    # This is done by grouping by 'District' and then shifting 'Temp_2m' by -1 (for the next day)
    if 'Temp_2m' in df.columns:
        df['Temp_2m_tomorrow'] = df.groupby('District')['Temp_2m'].shift(-1)
        print(" 'Temp_2m_tomorrow' column added successfully.")
    else:
        print("Error: 'Temp_2m' column not found. Cannot create target column.")
        return False

    # Optional: Display some rows with the new column to verify (first few and last few of a district)
    # This is for debugging/verification. You can comment it out later.
    print("\nSample data with 'Temp_2m_tomorrow' (first few rows):")
    print(df[['District', 'Date', 'Temp_2m', 'Temp_2m_tomorrow']].head())
    print("\nSample data with 'Temp_2m_tomorrow' (last few rows - showing NaNs at end of district):")
    print(df[['District', 'Date', 'Temp_2m', 'Temp_2m_tomorrow']].tail())


    # Save the dataset back, overwriting the input file as per plan.
    # Note: Rows without a value for the “next day” temp are kept for now,
    # they will be handled by the next step (04_drop_missing.py).
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"Data with target column saved to: {output_file}")
    print(f"Final shape: {df.shape}")
    print(f"Final columns (with target column):")
    print(df.columns.tolist())
    print(f"--- Finished 03_add_target_column.py ---")
    return True # Indicate success

if __name__ == "__main__":
    add_target_column()