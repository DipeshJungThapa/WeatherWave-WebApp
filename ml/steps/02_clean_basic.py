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
# from dotenv import load_dotenv # Removed
import os

# Load variables from ../.env (since you're in ml/steps and .env is in ml/)
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env')) # Removed
# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "ml-files"
INPUT_FILE = "filtered.csv"
OUTPUT_FILE = "cleaned_basic.csv"

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

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Perform basic cleaning on DataFrame"""
    try:
        # Rename 'Temperature_2m_tomorrow' to 'Temp_2m_tomorrow' if it exists
        if 'Temperature_2m_tomorrow' in df.columns:
            df.rename(columns={'Temperature_2m_tomorrow': 'Temp_2m_tomorrow'}, inplace=True)
            logger.info("Renamed 'Temperature_2m_tomorrow' to 'Temp_2m_tomorrow'.")
        else:
            logger.warning("'Temperature_2m_tomorrow' column not found for renaming.")

        # Ensure 'Date' column is datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        if df['Date'].isna().any():
            logger.warning(f"Found {df['Date'].isna().sum()} rows with invalid dates, dropping them.")
            df = df.dropna(subset=['Date'])

        # Ensure 'District' column is string type
        df['District'] = df['District'].astype(str)
        logger.info("'District' column ensured to be string type.")

        return df
    except Exception as e:
        logger.error(f"Data cleaning error: {str(e)}")
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
        logger.info(f"Successfully uploaded cleaned data to: {output_file}")
        # Check dtype before potentially accessing .dtype
        if 'Date' in df.columns:
             logger.info(f"Date column dtype in output: {df['Date'].dtype}")
        else:
             logger.warning("Date column not found in DataFrame after cleaning.")
        return True
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return False

def clean_basic_data() -> bool:
    """Main function to perform basic cleaning and upload to Supabase"""
    logger.info("Starting basic data cleaning process")

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

        # Clean DataFrame
        df_cleaned = clean_dataframe(df)
        if df_cleaned.empty:
            logger.error("No valid data after cleaning")
            return False

        logger.info(f"Final columns (after basic cleaning): {df_cleaned.columns.tolist()}")
        logger.info(f"Final shape: {df_cleaned.shape}")

        # Upload to Supabase
        return upload_to_supabase(supabase, df_cleaned, OUTPUT_FILE)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return False
    finally:
        logger.info("Finished basic data cleaning process")

if __name__ == "__main__":
    success = clean_basic_data()
    if success:
        logger.info("Script completed successfully!")
    else:
        logger.error("Script failed!")
