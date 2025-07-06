import pandas as pd
import os

input_file = 'ml/data/raw_data_processed.csv'
output_file = 'ml/data/filtered.csv'

print("--- Starting 01_filter_recent.py ---")

try:
    df = pd.read_csv(input_file)
    print(f"Loading data from: {input_file}")
    print(f"Initial shape: {df.shape}")

    # Convert 'Date' column to datetime objects
    df['Date'] = pd.to_datetime(df['Date'])

    # Define date range: from 5 years ago to 3 days before the most recent date
    most_recent_date = df['Date'].max()
    five_years_ago = most_recent_date - pd.DateOffset(years=5)
    three_days_back = most_recent_date - pd.Timedelta(days=2)

    # Filter the DataFrame to exclude the last 3 days
    df_filtered = df[(df['Date'] >= five_years_ago) & (df['Date'] <= three_days_back)]

    print(f"Filtered data from {five_years_ago.strftime('%Y-%m-%d')} to {three_days_back.strftime('%Y-%m-%d')}")
    print(f"Filtered shape: {df_filtered.shape}")

    df_filtered.to_csv(output_file, index=False)
    print(f"Filtered data saved to: {output_file}")

except FileNotFoundError:
    print(f"Error: The file '{input_file}' was not found. Please ensure raw_climate_data.csv is in the ml/data/ directory.")
except KeyError as e:
    print(f"Error: Required column not found - {e}. Please check the input CSV file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("--- Finished 01_filter_recent.py ---")
