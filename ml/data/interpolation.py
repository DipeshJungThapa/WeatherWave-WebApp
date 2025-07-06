import pandas as pd

file_path = "raw_data_processed.csv"

# Load data
df = pd.read_csv(file_path)

# Convert date
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d', errors='coerce')
df = df.sort_values(['District', 'Date']).reset_index(drop=True)

# Identify numeric columns
exclude_cols = ['District', 'Date', 'Latitude', 'Longitude']
numeric_cols = [col for col in df.columns if col not in exclude_cols]

# Interpolate per district
final_df = pd.DataFrame()
for district, group in df.groupby('District'):
    group = group.sort_values('Date').copy()
    group.set_index('Date', inplace=True)
    group[numeric_cols] = group[numeric_cols].interpolate(method='time', limit_direction='both')
    group.reset_index(inplace=True)
    final_df = pd.concat([final_df, group], axis=0)

# Sort and overwrite original file
final_df = final_df.sort_values(['District', 'Date']).reset_index(drop=True)
final_df.to_csv(file_path, index=False)

print("✅ Interpolation complete. File updated:", file_path)
