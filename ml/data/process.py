import io
import pandas as pd
from supabase import create_client
import numpy as np
import os

# --- Configuration ---
# Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "ml-files"
INPUT_FILE_PATH = "raw_data.csv"
OUTPUT_FILE_PATH = "raw_data_processed.csv"

# Invalid values from NASA POWER API
INVALID_VALUES = [-999, 999, -999.0, 999.0]

# --- Validation and Setup ---
if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("❌ SUPABASE_URL and SUPABASE_KEY must be set in environment variables.")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def validate_dataframe(df, required_columns=None):
    """Checks if a DataFrame is valid and has the required columns."""
    if df is None or df.empty:
        print("❌ Validation failed: DataFrame is empty.")
        return False

    if required_columns:
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"❌ Validation failed: Missing required columns: {missing_cols}")
            return False
    return True

# --- Data Processing Functions ---
def clean_weather_data(df):
    """Cleans weather data by handling invalid values and converting types."""
    print("🧹 Cleaning weather data...")
    
    # Identify weather parameter columns (i.e., not metadata)
    metadata_cols = ['Date', 'District', 'Latitude', 'Longitude']
    weather_cols = [col for col in df.columns if col not in metadata_cols]

    for col in weather_cols:
        # Convert to numeric, forcing errors to become NaN (missing)
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # Replace known invalid markers and infinity with NaN
        df[col] = df[col].replace(INVALID_VALUES + [np.inf, -np.inf], np.nan)

    # Assume missing precipitation is zero
    if 'Precip' in df.columns:
        precip_missing = df['Precip'].isna().sum()
        if precip_missing > 0:
            df['Precip'] = df['Precip'].fillna(0)
            print(f"   • Precip: Set {precip_missing} missing values to 0.")

    print("✅ Cleaning complete.")
    return df

# --- Supabase Interaction ---
def load_csv_from_supabase():
    """Loads the raw CSV data from the Supabase bucket."""
    print(f"⬇️  Downloading '{INPUT_FILE_PATH}' from bucket '{BUCKET_NAME}'...")
    try:
        data = supabase.storage.from_(BUCKET_NAME).download(INPUT_FILE_PATH)
        df = pd.read_csv(io.BytesIO(data), encoding='utf-8')
        print(f"✅ Successfully loaded {len(df)} records.")
        return df
    except Exception as e:
        print(f"❌ Failed to load CSV from Supabase. The file might not exist yet. Error: {e}")
        return None

def upload_csv_to_supabase(df):
    """Uploads the processed DataFrame as a CSV to Supabase, overwriting if it exists."""
    print(f"⬆️  Uploading '{OUTPUT_FILE_PATH}' to bucket '{BUCKET_NAME}'...")
    if not validate_dataframe(df, ['Date', 'District']):
        raise ValueError("Cannot upload invalid DataFrame.")

    try:
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode("utf-8")

        # Use "upsert: true" to automatically overwrite the file if it exists
        supabase.storage.from_(BUCKET_NAME).upload(
            OUTPUT_FILE_PATH,
            csv_bytes,
            {"content-type": "text/csv", "x-upsert": "true"}
        )
        print(f"✅ Successfully uploaded {len(df)} processed records.")
    except Exception as e:
        print(f"❌ Failed to upload CSV to Supabase. Error: {e}")
        raise

# --- Main Execution Logic ---
def process_data():
    """Main function to run the data processing pipeline."""
    print("\n--- 🚀 Starting Data Processing Step ---")

    df = load_csv_from_supabase()
    if df is None:
        print("🔴 No data loaded, exiting processing step.")
        return

    # Standardize column names for readability and consistency
    rename_map = {
        "DATE": "Date", "DISTRICT": "District", "LAT": "Latitude", "LON": "Longitude",
        "PRECTOT": "Precip", "PS": "Pressure", "QV2M": "SpecificHumidity", "RH2M": "RelativeHumidity",
        "T2M": "Temp", "T2MWET": "WetBulbTemp", "T2M_MAX": "MaxTemp", "T2M_MIN": "MinTemp",
        "TS": "EarthSkinTemp", "WS10M": "WindSpeed10m", "WS10M_MAX": "MaxWindSpeed10m",
        "WS10M_MIN": "MinWindSpeed10m", "WS50M": "WindSpeed50m", "WS50M_MAX": "MaxWindSpeed50m",
        "WS50M_MIN": "MinWindSpeed50m"
    }
    df = df.rename(columns=rename_map)
    print("ℹ️  Renamed columns for readability.")

    # Clean the data
    df = clean_weather_data(df)

    # Remove rows where all weather parameters are missing
    initial_count = len(df)
    weather_cols = [col for col in df.columns if col not in ['Date', 'District', 'Latitude', 'Longitude']]
    df.dropna(subset=weather_cols, how='all', inplace=True)
    removed_count = initial_count - len(df)
    if removed_count > 0:
        print(f"ℹ️  Removed {removed_count} rows with no weather data.")

    if df.empty:
        print("🔴 No valid data remaining after cleaning. Exiting.")
        return

    # Sort data for consistency before saving
    df = df.sort_values(['District', 'Date']).reset_index(drop=True)

    # Upload the final, processed data
    upload_csv_to_supabase(df)
    print("\n--- ✅ Data Processing Step Complete ---")

if __name__ == "__main__":
    process_data()