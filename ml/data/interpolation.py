import io
import pandas as pd
from supabase import create_client # Corrected import, 'storage' is not a top-level module
import numpy as np
import os

# Supabase credentials (use environment variables in production)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "ml-files"
INPUT_FILE_PATH = "raw_data_processed.csv"
OUTPUT_FILE_PATH = "raw_data_interpolated.csv"

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables.")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Invalid values that indicate missing/bad data
INVALID_VALUES = [-999, 999, -999.0, 999.0]

def validate_dataframe(df, required_columns=None):
    if df is None or df.empty:
        return False
    if required_columns:
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"Missing required columns: {missing_cols}")
            return False
    return True

def check_file_exists():
    try:
        files = supabase.storage.from_(BUCKET_NAME).list()
        file_names = [file["name"] for file in files]
        if INPUT_FILE_PATH not in file_names:
            print(f"File {INPUT_FILE_PATH} not found in bucket {BUCKET_NAME}")
            print(f"Available files: {file_names}")
            return False
        return True
    except Exception as e:
        print(f"Failed to list files in bucket: {e}")
        # Depending on your error handling strategy, you might want to raise the exception
        # raise
        return False

def load_csv_from_supabase():
    if not check_file_exists():
        return None
    try:
        data = supabase.storage.from_(BUCKET_NAME).download(INPUT_FILE_PATH)
        df = pd.read_csv(io.BytesIO(data), encoding='utf-8')

        if not validate_dataframe(df, ['Date', 'District']):
            print("Invalid DataFrame structure")
            return None

        print(f"CSV loaded from Supabase. Shape: {df.shape}")
        print(f"Sample Date values: {df['Date'].head().tolist()}")
        print(f"Date column type: {df['Date'].dtype}")
        print(f"Columns: {list(df.columns)}")
        return df

    except Exception as e:
        print(f"Failed to load CSV: {e}")
        # Depending on your error handling strategy, you might want to raise the exception
        # raise
        return None


def upload_csv_to_supabase(df):
    if not validate_dataframe(df, ['Date', 'District']):
        raise ValueError("Invalid DataFrame for upload")

    try:
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode("utf-8")

        # Refined error handling for file removal
        try:
            files = supabase.storage.from_(BUCKET_NAME).list()
            if any(file['name'] == OUTPUT_FILE_PATH for file in files):
                supabase.storage.from_(BUCKET_NAME).remove([OUTPUT_FILE_PATH])
                print(f"Removed existing file {OUTPUT_FILE_PATH}")
        except Exception as e:
            # Catch all potential errors during removal, e.g., file not found
            print(f"Error removing existing file (might not exist): {e}")

        supabase.storage.from_(BUCKET_NAME).upload(
            OUTPUT_FILE_PATH,
            csv_bytes,
            {"content-type": "text/csv"}
        )
        print(f"Successfully uploaded {len(df)} records to Supabase")

    except Exception as e:
        print(f"Failed to upload CSV: {e}")
        # Depending on your error handling strategy, you might want to raise the exception
        # raise


def interpolate_missing_values(group, numeric_cols):
    district_name = group['District'].iloc[0]
    missing_before = {col: group[col].isna().sum() for col in numeric_cols if col in group.columns}

    group_indexed = group.set_index('Date')

    for col in numeric_cols:
        if col in group_indexed.columns and col != 'Precip':
            group_indexed[col] = group_indexed[col].interpolate(
                method='time',
                limit_direction='both'
            )
            if group_indexed[col].isna().any():
                col_mean = group_indexed[col].mean()
                if not pd.isna(col_mean):
                    group_indexed[col] = group_indexed[col].fillna(col_mean)
                else:
                    group_indexed[col] = group_indexed[col].fillna(method='ffill').fillna(method='bfill')

    result = group_indexed.reset_index()

    missing_after = {col: result[col].isna().sum() for col in numeric_cols if col in result.columns}
    interpolated_count = sum(missing_before[col] - missing_after[col] for col in numeric_cols if col in result.columns)

    if interpolated_count > 0:
        print(f"{district_name}: Interpolated {interpolated_count} missing values")

    return result

def interpolate_data():
    print("Starting data interpolation...")

    df = load_csv_from_supabase()
    if df is None:
        print("No data loaded, exiting")
        return

    print(f"Processing {len(df)} records across {df['District'].nunique()} districts")

    try:
        df['Date'] = df['Date'].astype(str)
        sample_date = df['Date'].iloc[0]
        if len(sample_date) != 8:
            print(f"Warning: Expected YYYYMMDD format, got: {sample_date}")

        df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d', errors='coerce')
        print("Successfully parsed YYYYMMDD dates to datetime")

    except Exception as e:
        print(f"Date parsing failed: {e}")
        print("Sample dates:", df['Date'].head().tolist())
        return

    initial_count = len(df)
    df = df.dropna(subset=['Date', 'District'])
    if len(df) < initial_count:
        print(f"Removed {initial_count - len(df)} rows with invalid dates")

    if df.empty:
        print("No valid data remaining after date parsing")
        return

    exclude_cols = ['District', 'Date', 'Latitude', 'Longitude']
    numeric_cols = []

    for col in df.columns:
        if col not in exclude_cols:
            if pd.api.types.is_numeric_dtype(df[col]):
                numeric_cols.append(col)
            else:
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    numeric_cols.append(col)
                except:
                    print(f"Skipping non-numeric column: {col}")

    print(f"Interpolating {len(numeric_cols)} numeric columns: {numeric_cols}")

    for col in numeric_cols:
        if col != 'Precip':
            df[col] = df[col].replace(INVALID_VALUES, np.nan)

    print("\nMissing values before interpolation:")
    for col in numeric_cols:
        if col in df.columns:
            missing_count = df[col].isna().sum()
            if missing_count > 0:
                missing_pct = (missing_count / len(df)) * 100
                print(f"{col}: {missing_count} missing ({missing_pct:.1f}%)")

    final_df = pd.DataFrame()
    districts_processed = 0
    total_districts = df['District'].nunique()

    for district, group in df.groupby('District'):
        districts_processed += 1
        group = group.sort_values('Date').copy()
        group = group.drop_duplicates(subset=['Date'], keep='first')

        if len(group) < 2:
            print(f"Skipping {district} - insufficient data ({len(group)} records)")
            continue

        interpolated_group = interpolate_missing_values(group, numeric_cols)
        interpolated_group['Date'] = interpolated_group['Date'].dt.strftime('%Y%m%d')
        interpolated_group['District'] = district

        final_df = pd.concat([final_df, interpolated_group], axis=0, ignore_index=True)

        if districts_processed % 10 == 0:
            print(f"Processed {districts_processed}/{total_districts} districts...")

    if final_df.empty:
        print("No data after interpolation")
        return

    desired_columns = ['Date', 'District'] + [col for col in final_df.columns if col not in ['Date', 'District']]
    final_df = final_df[desired_columns]
    final_df = final_df.sort_values(['District', 'Date']).reset_index(drop=True)

    missing_dates = final_df['Date'].isna().sum()
    if missing_dates > 0:
        print(f"Warning: {missing_dates} missing dates in final result")

    print("\nMissing values after interpolation:")
    remaining_missing = False
    for col in numeric_cols:
        if col in final_df.columns:
            nan_count = final_df[col].isna().sum()
            if nan_count > 0:
                remaining_missing = True
                nan_pct = (nan_count / len(final_df)) * 100
                print(f"{col}: {nan_count} NaNs remain ({nan_pct:.1f}%)")

    if not remaining_missing:
        print("No missing values remaining")

    print("Interpolation complete")
    print(f"Final dataset: {len(final_df)} records across {final_df['District'].nunique()} districts")
    print(f"Final date format: YYYYMMDD strings")
    print(f"Sample final dates: {final_df['Date'].head().tolist()}")
    print(f"Date range: {final_df['Date'].min()} to {final_df['Date'].max()}")

    upload_csv_to_supabase(final_df)

if __name__ == "__main__":
    interpolate_data()
