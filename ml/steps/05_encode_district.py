import pandas as pd
import io
from supabase import create_client, Client, storage # Import storage explicitly
import logging
from datetime import datetime
import sys
from typing import Optional, Tuple
from sklearn.preprocessing import LabelEncoder
import joblib

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
INPUT_FILE = "no_missing.csv"
OUTPUT_FILE = "encoded_districts.csv"
OUTPUT_ENCODER_FILE = "label_encoder.pkl"

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
        sample_dates = df['Date'].dropna().head(5).tolist()
        for date in sample_dates:
            pd.to_datetime(date, format='%Y-%m-%d', errors='raise')
        logger.info("Date column format validated as YYYY-MM-DD")
    except ValueError as e:
        return False, f"Invalid date format in 'Date' column: {str(e)}. Expected YYYY-MM-DD."

    return True, ""

def encode_district(df: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[LabelEncoder]]:
    """Encode District column using LabelEncoder"""
    try:
        # Ensure 'Date' is datetime
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
        if df['Date'].isna().any():
            initial_rows = len(df)
            df = df.dropna(subset=['Date'])
            logger.warning(f"Dropped {initial_rows - len(df)} rows with invalid dates.")

        # Initialize and apply LabelEncoder
        le = LabelEncoder()
        df['District_encoded'] = le.fit_transform(df['District'])
        logger.info(f"Encoded 'District' column to 'District_encoded'.")
        logger.info(f"Unique encoded districts: {df['District_encoded'].nunique()}")

        return df, le
    except Exception as e:
        logger.error(f"Error encoding District column: {str(e)}")
        return pd.DataFrame(), None

def upload_to_supabase(supabase: Client, data: bytes, output_file: str, content_type: str) -> bool:
    """Upload data (CSV or pickle) to Supabase storage"""
    try:
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
            data,
            {"content-type": content_type}
        )
        logger.info(f"Successfully uploaded {output_file}")
        return True
    except Exception as e:
        logger.error(f"Upload error for {output_file}: {str(e)}")
        return False

def encode_district_data() -> bool:
    """Main function to encode District column and upload to Supabase"""
    logger.info("Starting district encoding process")

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

        # Encode District column
        df_encoded, le = encode_district(df)
        if df_encoded.empty or le is None:
            logger.error("No valid data after encoding or LabelEncoder creation failed")
            return False

        logger.info(f"Columns after encoding: {df_encoded.columns.tolist()}")
        logger.info(f"Final shape: {df_encoded.shape}")

        # Convert DataFrame to CSV bytes
        csv_buffer = io.StringIO()
        df_encoded.to_csv(csv_buffer, index=False, date_format='%Y-%m-%d')
        csv_bytes = csv_buffer.getvalue().encode("utf-8")

        # Save LabelEncoder to bytes
        encoder_buffer = io.BytesIO()
        joblib.dump(le, encoder_buffer)
        encoder_bytes = encoder_buffer.getvalue()

        # Upload both files to Supabase
        csv_success = upload_to_supabase(supabase, csv_bytes, OUTPUT_FILE, "text/csv")
        encoder_success = upload_to_supabase(supabase, encoder_bytes, OUTPUT_ENCODER_FILE, "application/octet-stream")

        return csv_success and encoder_success

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return False
    finally:
        logger.info("Finished district encoding process")

if __name__ == "__main__":
    success = encode_district_data()
    if success:
        logger.info("Script completed successfully!")
    else:
        logger.error("Script failed!")
