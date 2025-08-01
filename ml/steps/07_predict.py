import pandas as pd
import io
from supabase import create_client, Client
import logging
import sys
from typing import Optional, Tuple
import joblib
import os
import argparse
import json
import base64
from sklearn.preprocessing import LabelEncoder

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

# Google Drive config
SERVICE_ACCOUNT_INFO = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")  # From GitHub Secret
DRIVE_MODEL_FILE_ID = "1pGwE1lnHU-ZFWilY_ZivSCYFsrQASkZk"
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_drive_service():
    """Initialize Google Drive service with proper error handling"""
    try:
        if SERVICE_ACCOUNT_INFO:
            # If using GitHub Secrets (JSON string)
            try:
                # Try to decode if it's base64 encoded
                decoded_info = base64.b64decode(SERVICE_ACCOUNT_INFO).decode('utf-8')
                service_account_info = json.loads(decoded_info)
            except:
                # If not base64, treat as plain JSON string
                service_account_info = json.loads(SERVICE_ACCOUNT_INFO)
            
            creds = service_account.Credentials.from_service_account_info(
                service_account_info, scopes=SCOPES
            )
            logger.info("Using Google Drive credentials from environment variable")
        else:
            # Fallback to file-based authentication
            service_account_file = os.path.join(os.path.dirname(__file__), 'mldriveuploader.json')
            if not os.path.exists(service_account_file):
                raise FileNotFoundError(f"Service account file not found: {service_account_file}")
            
            creds = service_account.Credentials.from_service_account_file(
                service_account_file, scopes=SCOPES
            )
            logger.info("Using Google Drive credentials from local file")
        
        service = build('drive', 'v3', credentials=creds)
        return service
    except Exception as e:
        logger.error(f"Failed to initialize Google Drive service: {str(e)}")
        return None

def initialize_supabase() -> Optional[Client]:
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {str(e)}")
        return None

def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, str]:
    required_columns = ['Date', 'District', 'Temp_2m', 'Temp_2m_tomorrow', 'District_encoded'] + [col for col in MODEL_FEATURES if col != 'District_encoded']
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
        except Exception as e:
             # Handle API errors, e.g., file not found
             logger.warning(f"Error removing existing file (might not exist): {e}")

        supabase.storage.from_(BUCKET_NAME).upload(output_file, data, {"content-type": content_type})
        logger.info(f"Successfully uploaded {output_file}")
        return True
    except Exception as e:
        logger.error(f"Upload error for {output_file}: {str(e)}")
        return False

def download_model_from_drive() -> Optional[io.BytesIO]:
    try:
        service = get_drive_service()
        if not service:
            logger.error("Failed to initialize Google Drive service")
            return None

        logger.info("Starting model download from Google Drive")
        request = service.files().get_media(fileId=DRIVE_MODEL_FILE_ID)
        file_buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(file_buffer, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                logger.info(f"Downloading model from Drive: {int(status.progress() * 100)}%")

        file_buffer.seek(0)
        logger.info("Model download from Drive completed.")
        return file_buffer
    except Exception as e:
        logger.error(f"Failed to download model from Drive: {str(e)}")
        return None

def predict_weather() -> bool:
    logger.info("Starting prediction process")

    # Check authentication method
    if not SERVICE_ACCOUNT_INFO:
        service_account_file = os.path.join(os.path.dirname(__file__), 'mldriveuploader.json')
        if not os.path.exists(service_account_file):
            logger.error("No Google Drive authentication found!")
            logger.error("Either set GOOGLE_SERVICE_ACCOUNT_JSON environment variable")
            logger.error("or ensure 'mldriveuploader.json' is in the same directory as the script.")
            return False
        else:
            logger.info("Using local service account file for authentication")
    else:
        logger.info("Using environment variable for Google Drive authentication")

    supabase = initialize_supabase()
    if not supabase:
        logger.error("Failed to initialize Supabase client")
        return False

    try:
        # Download model file from Google Drive
        logger.info("Downloading model from Google Drive")
        model_file_bytes = download_model_from_drive()
        if model_file_bytes is None:
            logger.error("Failed to download model file from Google Drive.")
            return False

        # Load model from in-memory bytes buffer
        model = joblib.load(model_file_bytes)
        logger.info("Model loaded successfully from Google Drive.")

        # Load label encoder
        logger.info("Loading label encoder from Supabase")
        label_encoder = load_label_encoder(supabase)
        if label_encoder is None:
            logger.error("Failed to load label encoder")
            return False

        # Load input data
        logger.info(f"Downloading {INPUT_FILE} from Supabase")
        response = supabase.storage.from_(BUCKET_NAME).download(INPUT_FILE)
        if not response:
            logger.error(f"Could not fetch {INPUT_FILE} from Supabase bucket")
            return False

        df = pd.read_csv(io.BytesIO(response))
        logger.info(f"Loaded data from Supabase: {INPUT_FILE}")
        logger.info(f"Data shape: {df.shape}")

        # Validate data
        valid, msg = validate_dataframe(df)
        if not valid:
            logger.error(f"Data validation failed: {msg}")
            return False

        # Make predictions
        logger.info("Starting prediction process")
        df_pred = make_predictions(df, model, label_encoder)
        if df_pred.empty:
            logger.error("Prediction failed")
            return False

        # Save predictions
        logger.info("Saving predictions to Supabase")
        csv_buffer = io.StringIO()
        df_pred.to_csv(csv_buffer, index=False, date_format='%Y-%m-%d')
        csv_bytes = csv_buffer.getvalue().encode("utf-8")

        success = upload_to_supabase(supabase, csv_bytes, OUTPUT_FILE, "text/csv")
        if success:
            logger.info(f"Predictions successfully saved to {OUTPUT_FILE}")
        return success

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
