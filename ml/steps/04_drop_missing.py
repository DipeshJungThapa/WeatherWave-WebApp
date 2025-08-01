import pandas as pd
import io
from supabase import create_client, Client
import logging
from datetime import datetime
import sys
from typing import Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Supabase credentials
# from dotenv import load_dotenv # Removed
import os

# Load variables from ../.env (since you're in ml/steps and .env is in ml/)
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env')) # Removed
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "ml-files"
INPUT_FILE = "with_target.csv"
OUTPUT_FILE = "no_missing.csv"

def initialize_supabase() -> Optional[Client]:
    """Initialize and return Supabase client with error handling"""
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {str(e)}")
        return None

def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, str]:
    """Validate DataFrame structure and required columns"""
    required_columns = ['Date', 'District', 'Temp_2m', 'Temp_2m_tomorrow']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"

    if df.empty:
        return False, "DataFrame is empty"

    # Validate Date format
    try:
        # Sample a few non-null dates to check format
        sample_dates = df['Date'].dropna().head(5).tolist()
        for date in sample_dates:
            pd.to_datetime(date, format='%Y-%m-%d', errors='raise')
        logger.info("Date column format validated as YYYY-MM-DD")
    except ValueError as e:
        return False, f"Invalid date format in 'Date' column: {str(e)}. Expected YYYY-MM-DD."

    return True, ""

def drop_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with any missing values"""
    try:
        # Ensure 'Date' is datetime
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
        if df['Date'].isna().any():
            initial_rows = len(df)
            df = df.dropna(subset=['Date'])
            logger.warning(f"Dropped {initial_rows - len(df)} rows with invalid dates.")

        # Drop rows with any missing values
        initial_rows = len(df)
        df = df.dropna()
        rows_dropped = initial_rows - len(df)
        if rows_dropped > 0:
            logger.info(f"Dropped {rows_dropped} rows with missing values.")
        else:
            logger.info("No rows with missing values found.")

        return df
    except Exception as e:
        logger.error(f"Error dropping missing values: {str(e)}")
        return pd.DataFrame()

def upload_to_supabase(supabase: Client, df: pd.DataFrame, output_file: str) -> bool:
    """Upload DataFrame to Supabase storage with Date as datetime"""
    try:
        # Convert to CSV bytes, keeping Date as datetime (YYYY-MM-DD)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, date_format='%Y-%m-%d')
        csv_bytes = csv_buffer.getvalue().encode("utf-8")

        # Remove existing file if it exists
        try:
            files = supabase.storage.from_(BUCKET_NAME).list()
            if any(file['name'] == output_file for file in files):
                supabase.storage.from_(BUCKET_NAME).remove([output_file])
                logger.info(f"Removed existing file: {output_file}")
        except Exception as e:
             # Handle API errors, e.g., file not found
             logger.warning(f"Error removing existing file (might not exist): {e}")

        # Upload file
        supabase.storage.from_(BUCKET_NAME).upload(
            output_file,
            csv_bytes,
            {"content-type": "text/csv"}
        )
        logger.info(f"Successfully uploaded data with no missing values to: {output_file}")
        # Check dtype before potentially accessing .dtype
        if 'Date' in df.columns:
             logger.info(f"Date column dtype in output: {df['Date'].dtype}")
        else:
             logger.warning("Date column not found in DataFrame after dropping missing.")
        return True
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return False

def drop_missing_data() -> bool:
    """Main function to drop missing values and upload to Supabase"""
    logger.info("Starting missing values removal process")

    # Initialize Supabase client
    supabase = initialize_supabase()
    if not supabase:
        return False

    try:
        # Fetch CSV from Supabase
        response = supabase.storage.from_(BUCKET_NAME).download(INPUT_FILE)
        if not response:
            logger.error(f"Could not fetch {INPUT_FILE} from Supabase bucket")
            return False

        # Read and validate DataFrame
        df = pd.read_csv(io.BytesIO(response))
        logger.info(f"Loaded data from Supabase: {INPUT_FILE}")
        logger.info(f"Initial shape: {df.shape}")
        logger.info(f"Columns: {list(df.columns)}")
        # Check if 'Date' column exists before accessing head()
        if 'Date' in df.columns:
             logger.info(f"Sample Date values: {df['Date'].head().tolist()}")
        else:
             logger.warning("Date column not found in loaded DataFrame.")

        is_valid, validation_message = validate_dataframe(df)
        if not is_valid:
            logger.error(validation_message)
            return False

        # Drop missing values
        df_cleaned = drop_missing_values(df)
        if df_cleaned.empty:
            logger.error("No valid data after dropping missing values")
            return False

        logger.info(f"Final shape after dropping missing: {df_cleaned.shape}")

        # Upload to Supabase
        return upload_to_supabase(supabase, df_cleaned, OUTPUT_FILE)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return False
    finally:
        logger.info("Finished missing values removal process")

if __name__ == "__main__":
    success = drop_missing_data()
    if success:
        logger.info("Script completed successfully!")
    else:
        logger.error("Script failed!")
