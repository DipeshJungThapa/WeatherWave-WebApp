import pandas as pd

input_file = "raw_data.csv"
output_file = "raw_data_processed.csv"

# Load data
df = pd.read_csv(input_file)

# Rename columns
rename_map = {
    "DATE": "Date", "DISTRICT": "District", "LAT": "Latitude", "LON": "Longitude",
    "PRECTOT": "Precip", "PS": "Pressure", "QV2M": "Humidity_2m", "RH2M": "RH_2m",
    "T2M": "Temp_2m", "T2MWET": "WetBulbTemp_2m", "T2M_MAX": "MaxTemp_2m", "T2M_MIN": "MinTemp_2m",
    "TS": "EarthSkinTemp", "WS10M": "WindSpeed_10m", "WS10M_MAX": "MaxWindSpeed_10m",
    "WS10M_MIN": "MinWindSpeed_10m", "WS50M": "WindSpeed_50m", "WS50M_MAX": "MaxWindSpeed_50m",
    "WS50M_MIN": "MinWindSpeed_50m"
}
df = df.rename(columns=rename_map)

# Force Precip = 0
df['Precip'] = 0


# Save the result
df.to_csv(output_file, index=False)
print("✅ Column renaming and feature calculation complete. Saved as:", output_file)
