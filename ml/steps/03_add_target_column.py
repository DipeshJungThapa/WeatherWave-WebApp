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
from dotenv import load_dotenv
import os

# Load variables from ../.env (since you're in ml/steps and .env is in ml/)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "ml-files"
INPUT_FILE = "cleaned_basic.csv"
OUTPUT_FILE = "with_target.csv"

def initialize_supabase() -> Optional[Client]:
    """Initialize and return Supabase client with error handling"""
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {str(e)}")
        return None

def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, str]:
    """Validate DataFrame structure and required columns"""
    required_columns = ['Date', 'District', 'Temp_2m']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    if df.empty:
        return False, "DataFrame is empty"
    
    return True, ""

def add_target_column(df: pd.DataFrame) -> pd.DataFrame:
    """Add Temp_2m_tomorrow target column by shifting Temp_2m within District groups"""
    try:
        # Ensure 'Date' is datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        if df['Date'].isna().any():
            logger.warning(f"Found {df['Date'].isna().sum()} rows with invalid dates, dropping them.")
            df = df.dropna(subset=['Date'])

        # Sort by District and Date for correct shifting
        df = df.sort_values(by=['District', 'Date']).reset_index(drop=True)

        # Create target column by shifting Temp_2m within each District
        df['Temp_2m_tomorrow'] = df.groupby('District')['Temp_2m'].shift(-1)

        # Drop rows where Temp_2m_tomorrow is NaN
        initial_rows = df.shape[0]
        df = df.dropna(subset=['Temp_2m_tomorrow'])
        rows_dropped = initial_rows - df.shape[0]
        if rows_dropped > 0:
            logger.info(f"Dropped {rows_dropped} rows due to missing 'Temp_2m_tomorrow' values (end of district data).")

        return df
    except Exception as e:
        logger.error(f"Target column creation error: {str(e)}")
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
            logger.warning(f"Could not check/remove existing file: {str(e)}")

        # Upload file
        supabase.storage.from_(BUCKET_NAME).upload(
            output_file,
            csv_bytes,
            {"content-type": "text/csv"}
        )
        logger.info(f"Successfully uploaded data with target to: {output_file}")
        logger.info(f"Date column dtype in output: {df['Date'].dtype}")
        return True
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return False

def add_target_data() -> bool:
    """Main function to add target column and upload to Supabase"""
    logger.info("Starting target column addition process")

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
        logger.info(f"Sample Date values: {df['Date'].head().tolist()}")

        is_valid, validation_message = validate_dataframe(df)
        if not is_valid:
            logger.error(validation_message)
            return False

        # Add target column
        df_with_target = add_target_column(df)
        if df_with_target.empty:
            logger.error("No valid data after adding target column")
            return False

        logger.info(f"Columns after adding target: {df_with_target.columns.tolist()}")
        logger.info(f"Final shape: {df_with_target.shape}")

        # Upload to Supabase
        return upload_to_supabase(supabase, df_with_target, OUTPUT_FILE)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return False
    finally:
        logger.info("Finished target column addition process")

if __name__ == "__main__":
    success = add_target_data()
    if success:
        logger.info("Script completed successfully!")
    else:
        logger.error("Script failed!")