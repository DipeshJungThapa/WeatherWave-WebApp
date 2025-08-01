import io
import pandas as pd
from supabase import create_client, storage # Import storage explicitly
import numpy as np
# from dotenv import load_dotenv # Removed
import os

# Supabase credentials from environment variables (set in GitHub Actions secrets)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "ml-files"
INPUT_FILE_PATH = "raw_data.csv"
OUTPUT_FILE_PATH = "raw_data_processed.csv"

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables.")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Invalid values that indicate missing/bad data (matching fetchdata.py)
INVALID_VALUES = [-999, 999, -999.0, 999.0]

def validate_dataframe(df, required_columns=None):
    """Validate DataFrame structure and content"""
    if df is None or df.empty:
        return False

    if required_columns:
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"❌ Missing required columns: {missing_cols}")
            return False

    return True

def is_valid_value(value):
    """Check if a value is valid (not missing, not invalid, not empty)"""
    if pd.isna(value) or value == '' or value is None:
        return False

    if value in INVALID_VALUES:
        return False

    try:
        float_val = float(value)
        return not (np.isinf(float_val) or np.isnan(float_val))
    except (ValueError, TypeError):
        return False

def clean_weather_data(df):
    """Clean weather data by handling invalid values and empty cells"""
    print(" Cleaning weather data...")

    # Identify weather parameter columns (exclude metadata columns)
    metadata_cols = ['Date', 'District', 'Latitude', 'Longitude']
    weather_cols = [col for col in df.columns if col not in metadata_cols]

    cleaned_count = 0

    for col in weather_cols:
        if col in df.columns:
            original_invalid = df[col].isna().sum()

            # Handle different types of invalid data
            # 1. Replace explicit invalid values with NaN
            df[col] = df[col].replace(INVALID_VALUES, np.nan)

            # 2. Handle empty strings and whitespace
            df[col] = df[col].replace(['', ' ', '  '], np.nan)

            # 3. Convert to numeric, coercing errors to NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')

            # 4. Handle infinite values
            df[col] = df[col].replace([np.inf, -np.inf], np.nan)

            # Special handling for precipitation - set invalid/missing to 0
            if col == 'Precip':
                df[col] = df[col].fillna(0)
                print(f"   • {col}: Set missing values to 0 (no precipitation)")
            else:
                new_invalid = df[col].isna().sum()
                if new_invalid != original_invalid:
                    print(f"   • {col}: {new_invalid - original_invalid} additional invalid values found")
                    cleaned_count += 1

    print(f" Cleaned {cleaned_count} weather parameter columns")
    return df

def load_csv_from_supabase():
    """Load CSV from Supabase with improved error handling"""
    try:
        data = supabase.storage.from_(BUCKET_NAME).download(INPUT_FILE_PATH)
        df = pd.read_csv(io.BytesIO(data), encoding='utf-8')

        if not validate_dataframe(df):
            print(" Invalid DataFrame loaded")
            return None

        print(f" CSV loaded from Supabase. Shape: {df.shape}")
        print(f" Sample DATE values: {df['DATE'].head().tolist()}")
        print(f"Columns: {list(df.columns)}")

        return df

    except Exception as e:
        print(f"❌ Failed to load CSV: {e}")
        # Depending on your error handling strategy, you might want to raise the exception
        # raise
        return None

def upload_csv_to_supabase(df):
    """Upload CSV to Supabase with improved error handling"""
    if not validate_dataframe(df, ['Date', 'District']):
        raise ValueError("Invalid DataFrame for upload")

    try:
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode("utf-8")

        # Remove existing file if it exists
        try:
            files = supabase.storage.from_(BUCKET_NAME).list()
            if any(file['name'] == OUTPUT_FILE_PATH for file in files):
                supabase.storage.from_(BUCKET_NAME).remove([OUTPUT_FILE_PATH])
                print(f" Removed existing file {OUTPUT_FILE_PATH}")
        except storage.PostgrestAPIError as e:
             # Handle specific API errors, e.g., file not found
             print(f"Error removing existing file (might not exist): {e}")
        except Exception as e:
             # Catch other potential errors during removal
             print(f"An unexpected error occurred during file removal: {e}")


        response = supabase.storage.from_(BUCKET_NAME).upload(
            OUTPUT_FILE_PATH,
            csv_bytes,
            {"content-type": "text/csv"}
        )

        print(f" Successfully uploaded {len(df)} records to Supabase")

    except Exception as e:
        print(f" Failed to upload CSV: {e}")
        # Depending on your error handling strategy, you might want to raise the exception
        # raise


def process_data():
    """Process raw weather data maintaining YYYYMMDD date format"""
    print(" Starting data processing...")

    # Load data from Supabase
    df = load_csv_from_supabase()
    if df is None:
        print(" No data loaded, exiting")
        return

    print(f" Processing {len(df)} records")

    # Validate that required columns exist
    required_cols = ['DATE', 'DISTRICT']
    missing_required = [col for col in required_cols if col not in df.columns]
    if missing_required:
        print(f" Missing required columns: {missing_required}")
        return

    # Ensure DATE is string format for consistency (matching fetchdata.py approach)
    df['DATE'] = df['DATE'].astype(str)

    # Validate date format
    sample_date = df['DATE'].iloc[0]
    if len(sample_date) != 8:
        print(f" Warning: DATE format might not be YYYYMMDD. Sample: {sample_date}")
    else:
        print(f" DATE format validated: YYYYMMDD (sample: {sample_date})")

    # Column renaming with validation
    rename_map = {
        "DATE": "Date",
        "DISTRICT": "District",
        "LAT": "Latitude",
        "LON": "Longitude",
        "PRECTOT": "Precip",
        "PS": "Pressure",
        "QV2M": "Humidity_2m",
        "RH2M": "RH_2m",
        "T2M": "Temp_2m",
        "T2MWET": "WetBulbTemp_2m",
        "T2M_MAX": "MaxTemp_2m",
        "T2M_MIN": "MinTemp_2m",
        "TS": "EarthSkinTemp",
        "WS10M": "WindSpeed_10m",
        "WS10M_MAX": "MaxWindSpeed_10m",
        "WS10M_MIN": "MinWindSpeed_10m",
        "WS50M": "WindSpeed_50m",
        "WS50M_MAX": "MaxWindSpeed_50m",
        "WS50M_MIN": "MinWindSpeed_50m"
    }

    # Only rename columns that exist
    existing_columns = {old: new for old, new in rename_map.items() if old in df.columns}
    df = df.rename(columns=existing_columns)

    print(f" Renamed {len(existing_columns)} columns")

    # Clean weather data (handle invalid values, empty cells, etc.)
    df = clean_weather_data(df)

    # Data quality assessment
    print("\n Data Quality Summary:")
    print(f"   • Total records: {len(df)}")
    print(f"   • Districts: {df['District'].nunique() if 'District' in df.columns else 'N/A'}")
    print(f"   • Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"   • Date format: YYYYMMDD (kept as strings)")

    # Count valid records per key parameter
    key_params = ['Temp_2m', 'RH_2m', 'Pressure']
    for param in key_params:
        if param in df.columns:
            valid_count = df[param].notna().sum()
            valid_pct = (valid_count / len(df)) * 100
            print(f"   • {param}: {valid_count}/{len(df)} valid ({valid_pct:.1f}%)")

    # Check for missing values
    missing_summary = df.isnull().sum()
    if missing_summary.any():
        print("\n Missing values detected:")
        for col, count in missing_summary[missing_summary > 0].items():
            pct = (count / len(df)) * 100
            print(f"   • {col}: {count} missing values ({pct:.1f}%)")

    # Remove rows where all weather parameters are missing
    weather_cols = [col for col in df.columns if col not in ['Date', 'District', 'Latitude', 'Longitude']]
    initial_count = len(df)
    df = df.dropna(subset=weather_cols, how='all')
    removed_count = initial_count - len(df)

    if removed_count > 0:
        print(f" Removed {removed_count} rows with no valid weather data")

    # Validate final data
    if not validate_dataframe(df, ['Date', 'District']):
        print(" Final validation failed")
        return

    if df.empty:
        print(" No data remaining after processing")
        return

    # Sort data for consistency
    df = df.sort_values(['District', 'Date']).reset_index(drop=True)

    # Upload the result to Supabase
    upload_csv_to_supabase(df)
    print(f" Processing complete. Data saved as: {OUTPUT_FILE_PATH}")
    print(f"Final dataset: {len(df)} records across {df['District'].nunique()} districts")

if __name__ == "__main__":
    process_data()
