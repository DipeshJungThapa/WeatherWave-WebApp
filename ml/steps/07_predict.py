import pandas as pd
import io
from supabase import create_client, Client, storage # Import storage explicitly
import logging
import sys
from typing import Optional, Tuple
import joblib
import os
import argparse
from sklearn.preprocessing import LabelEncoder
# from dotenv import load_dotenv # Removed

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Load environment variables (adjust path as needed)
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env')) # Removed

# Constants and config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "ml-files"
INPUT_FILE = "encoded_districts.csv"
OUTPUT_FILE = "predictions.csv"
LABEL_ENCODER_PATH = "label_encoder.pkl"

MODEL_FEATURES = [
    'Latitude', 'Longitude', 'Precip', 'Pressure', 'Humidity_2m', 'RH_2m',
    'Temp_2m', 'WetBulbTemp_2m', 'MaxTemp_2m', 'MinTemp_2m', 'EarthSkinTemp',
    'WindSpeed_10m', 'MaxWindSpeed_10m', 'MinWindSpeed_10m',
    'WindSpeed_50m', 'MaxWindSpeed_50m', 'MinWindSpeed_50m',
    'District_encoded'
]

# Google Drive config - Path is relative to the script
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), 'mldriveuploader.json')

DRIVE_MODEL_FILE_ID = "1pGwE1lnHU-ZFWilY_ZivSCYFsrQASkZk"

def initialize_supabase() -> Optional[Client]:
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {str(e)}")
        return None

def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, str]:
    required_columns = ['Date', 'District', 'Temp_2m', 'Temp_2m_tomorrow', 'District_encoded'] + [col for col in MODEL_FEATURES if col != 'District_encoded'] # Adjust required columns check
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    if df.empty:
        return False, "DataFrame is empty"
    try:
        sample_dates = df['Date'].dropna().head(5)
        for date in sample_dates:
            pd.to_datetime(date, format='%Y-%m-%d', errors='raise')
        logger.info("Date column format validated as YYYY-MM-DD")
    except ValueError as e:
        return False, f"Invalid date format in 'Date' column: {str(e)}. Expected YYYY-MM-DD."
    return True, ""

def load_label_encoder(supabase: Client) -> Optional[LabelEncoder]:
    try:
        response = supabase.storage.from_(BUCKET_NAME).download(LABEL_ENCODER_PATH)
        if not response:
            logger.error(f"Could not fetch {LABEL_ENCODER_PATH} from Supabase bucket")
            return None
        encoder = joblib.load(io.BytesIO(response))
        logger.info(f"Loaded label encoder from Supabase: {LABEL_ENCODER_PATH}")
        return encoder
    except Exception as e:
        logger.error(f"Error loading label encoder from Supabase: {str(e)}")
        return None

def make_predictions(df: pd.DataFrame, model, label_encoder: LabelEncoder) -> pd.DataFrame:
    try:
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
        if df['Date'].isna().any():
            dropped = df['Date'].isna().sum()
            df = df.dropna(subset=['Date'])
            logger.warning(f"Dropped {dropped} rows with invalid dates.")

        # Ensure all MODEL_FEATURES exist before selecting
        missing_features = [col for col in MODEL_FEATURES if col not in df.columns]
        if missing_features:
            logger.error(f"Missing features for prediction: {', '.join(missing_features)}")
            return pd.DataFrame()

        X = df[MODEL_FEATURES].astype('float32')
        predictions = model.predict(X)
        df['predicted_Temp_2m_tomorrow'] = predictions
        logger.info(f"Batch predictions completed for {len(df)} samples")

        # Show latest Kathmandu prediction (encoded value = 35)
        kathmandu_encoded_val = 35
        if 'District_encoded' in df.columns:
            kathmandu_rows = df[df['District_encoded'] == kathmandu_encoded_val]
            if kathmandu_rows.empty:
                logger.warning("No Kathmandu data found for latest prediction display.")
            else:
                latest_date = kathmandu_rows['Date'].max()
                latest_pred = kathmandu_rows[kathmandu_rows['Date'] == latest_date]
                cols_to_show = ['Date', 'District', 'Temp_2m_tomorrow', 'predicted_Temp_2m_tomorrow']
                # Check if columns exist before trying to select them
                cols_to_show = [col for col in cols_to_show if col in latest_pred.columns]
                if cols_to_show:
                     logger.info("\n--- Latest Kathmandu Prediction ---")
                     logger.info(latest_pred[cols_to_show].to_string(index=False))
                     logger.info("--- End of Kathmandu Prediction ---")
                else:
                     logger.warning("Required columns for Kathmandu prediction display not found.")
        else:
            logger.warning("'District_encoded' column not found, skipping Kathmandu prediction display.")


        return df
    except Exception as e:
        logger.error(f"Error making predictions: {str(e)}")
        return pd.DataFrame()

def upload_to_supabase(supabase: Client, data: bytes, output_file: str, content_type: str) -> bool:
    try:
        try:
            files = supabase.storage.from_(BUCKET_NAME).list()
            if any(f['name'] == output_file for f in files):
                supabase.storage.from_(BUCKET_NAME).remove([output_file])
                logger.info(f"Removed existing file: {output_file}")
        except storage.PostgrestAPIError as e:
             # Handle specific API errors, e.g., file not found
             logger.warning(f"Error removing existing file (might not exist): {e}")
        except Exception as e:
             # Catch other potential errors during removal
             logger.warning(f"An unexpected error occurred during file removal: {e}")


        supabase.storage.from_(BUCKET_NAME).upload(output_file, data, {"content-type": content_type})
        logger.info(f"Successfully uploaded {output_file}")
        return True
    except Exception as e:
        logger.error(f"Upload error for {output_file}: {str(e)}")
        return False

def download_model_from_drive(service_account_file: str, file_id: str) -> Optional[io.BytesIO]:
    try:
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        service = build('drive', 'v3', credentials=credentials)
        request = service.files().get_media(fileId=file_id)
        file_buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(file_buffer, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            logger.info(f"Downloading model from Drive: {int(status.progress() * 100)}%")

        file_buffer.seek(0)
        logger.info("Model download from Drive completed.")
        return file_buffer
    except Exception as e:
        logger.error(f"Failed to download model from Drive: {str(e)}")
        return None

def predict_weather() -> bool:
    logger.info("Starting prediction process")

    # Check if the service account file exists (if not using GitHub Secret method)
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        logger.error(f"Google Drive service account key file not found at: {SERVICE_ACCOUNT_FILE}")
        logger.error("Please ensure 'mldriveuploader.json' is in the same directory as the script.")
        return False


    supabase = initialize_supabase()
    if not supabase:
        return False

    try:
        # Download model file from Google Drive
        model_file_bytes = download_model_from_drive(SERVICE_ACCOUNT_FILE, DRIVE_MODEL_FILE_ID)
        if model_file_bytes is None:
            logger.error("Failed to download model file from Google Drive.")
            return False

        # Load model from in-memory bytes buffer
        model = joblib.load(model_file_bytes)
        logger.info("Model loaded successfully from Google Drive.")

        label_encoder = load_label_encoder(supabase)
        if label_encoder is None:
            return False

        response = supabase.storage.from_(BUCKET_NAME).download(INPUT_FILE)
        if not response:
            logger.error(f"Could not fetch {INPUT_FILE} from Supabase bucket")
            return False

        df = pd.read_csv(io.BytesIO(response))
        logger.info(f"Loaded data from Supabase: {INPUT_FILE}")
        logger.info(f"Data shape: {df.shape}")

        valid, msg = validate_dataframe(df)
        if not valid:
            logger.error(msg)
            return False

        df_pred = make_predictions(df, model, label_encoder)
        if df_pred.empty:
            logger.error("Prediction failed")
            return False

        csv_buffer = io.StringIO()
        df_pred.to_csv(csv_buffer, index=False, date_format='%Y-%m-%d')
        csv_bytes = csv_buffer.getvalue().encode("utf-8")

        return upload_to_supabase(supabase, csv_bytes, OUTPUT_FILE, "text/csv")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return False
    finally:
        logger.info("Finished prediction process")

if __name__ == "__main__":

    success = predict_weather()
    if success:
        logger.info("Script completed successfully!")
    else:
        logger.error("Script failed!")
