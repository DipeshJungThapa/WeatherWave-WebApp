import pandas as pd
import io
from supabase import create_client, Client, storage # Import storage explicitly
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
INPUT_FILE = "raw_data_interpolated.csv"
OUTPUT_FILE = "filtered.csv"

def initialize_supabase() -> Optional[Client]:
    """Initialize and return Supabase client with error handling"""
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {str(e)}")
        return None

def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, str]:
    """Validate DataFrame structure and required columns"""
    required_columns = ['Date', 'District']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"

    if df.empty:
        return False, "DataFrame is empty"

    return True, ""

def convert_dates(df: pd.DataFrame) -> Tuple[pd.DataFrame, bool]:
    """Convert dates and handle invalid entries"""
    try:
        df['Date'] = df['Date'].astype(str)
        df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d', errors='coerce')

        initial_count = len(df)
        df = df.dropna(subset=['Date'])
        success = len(df) > 0

        if initial_count > len(df):
            logger.warning(f"Removed {initial_count - len(df)} rows with invalid dates")

        return df, success
    except Exception as e:
        logger.error(f"Date conversion error: {str(e)}")
        return df, False

def filter_date_range(df: pd.DataFrame) -> pd.DataFrame:
    """Filter DataFrame to last 5 years"""
    try:
        most_recent = df['Date'].max()
        five_years_ago = most_recent - pd.DateOffset(years=5)

        logger.info(f"Most recent date: {most_recent.date()}")
        logger.info(f"Five years ago: {five_years_ago.date()}")

        df_filtered = df[df['Date'] >= five_years_ago]
        return df_filtered
    except Exception as e:
        logger.error(f"Date range filtering error: {str(e)}")
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
        except storage.PostgrestAPIError as e:
             # Handle specific API errors, e.g., file not found
             logger.warning(f"Error removing existing file (might not exist): {e}")
        except Exception as e:
             # Catch other potential errors during removal
             logger.warning(f"An unexpected error occurred during file removal: {e}")


        # Upload file
        supabase.storage.from_(BUCKET_NAME).upload(
            output_file,
            csv_bytes,
            {"content-type": "text/csv"}
        )
        logger.info(f"Successfully uploaded filtered data to: {output_file}")
        # Check dtype before potentially accessing .dtype
        if 'Date' in df.columns:
            logger.info(f"Date column dtype in output: {df['Date'].dtype}")
        else:
            logger.warning("Date column not found in DataFrame after filtering.")

        return True
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return False

def filter_recent_data() -> bool:
    """Main function to filter data to last 5 years"""
    logger.info("Starting data filtering process")

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

        # Convert and validate dates
        df, date_success = convert_dates(df)
        if not date_success:
            logger.error("No valid data after date parsing")
            return False

        # Filter date range
        df_filtered = filter_date_range(df)
        logger.info(f"Filtered shape: {df_filtered.shape}")

        if not df_filtered.empty:
            # Check if 'District' and 'Date' columns exist before accessing them
            if 'District' in df_filtered.columns:
                logger.info(f"Districts in filtered data: {df_filtered['District'].nunique()}")
            else:
                logger.warning("District column not found in filtered DataFrame.")
            if 'Date' in df_filtered.columns:
                 logger.info(f"Date range in filtered data: {df_filtered['Date'].min().date()} to {df_filtered['Date'].max().date()}")
            else:
                 logger.warning("Date column not found in filtered DataFrame.")

        else:
            logger.warning("No data in the specified date range")

        # Upload to Supabase
        return upload_to_supabase(supabase, df_filtered, OUTPUT_FILE)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return False
    finally:
        logger.info("Finished data filtering process")

if __name__ == "__main__":
    success = filter_recent_data()
    if success:
        logger.info("Script completed successfully!")
    else:
        logger.error("Script failed!")
