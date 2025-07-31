import pandas as pd
import io
from supabase import create_client, Client, storage
import logging
import sys
from typing import Optional, Tuple
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
# from dotenv import load_dotenv # Removed
from googleapiclient.errors import HttpError

# Google Drive API imports for service account
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Load environment variables
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env')) # Removed

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "ml-files"
INPUT_FILE = "encoded_districts.csv"
TARGET_COLUMN = "Temp_2m_tomorrow"
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Google Drive service account configuration - Path is relative to the script
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), 'mldriveuploader.json')
DRIVE_FILE_ID = "1pGwE1lnHU-ZFWilY_ZivSCYFsrQASkZk"
SCOPES = ['https://www.googleapis.com/auth/drive']

def initialize_supabase() -> Optional[Client]:
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {str(e)}")
        return None

def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, str]:
    required_columns = ['Date', 'District', 'Temp_2m', 'Temp_2m_tomorrow', 'District_encoded']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        return False, f"Missing required columns: {', '.join(missing)}"
    if df.empty:
        return False, "DataFrame is empty"
    try:
        sample_dates = df['Date'].dropna().head(5)
        for date in sample_dates:
            pd.to_datetime(date, format='%Y-%m-%d', errors='raise')
        logger.info("Date column format validated as YYYY-MM-DD")
    except ValueError as e:
        return False, f"Invalid date format in 'Date': {str(e)}"
    return True, ""

def train_model(df: pd.DataFrame) -> Tuple[Optional[RandomForestRegressor], float, float]:
    try:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['Date'], inplace=True)

        excluded = ['Date', 'District', TARGET_COLUMN, 'Unnamed: 0']
        features = [c for c in df.columns if c not in excluded]
        if 'District_encoded' in df.columns and 'District_encoded' not in features:
            features.append('District_encoded')

        X = df[features].astype('float32')
        y = df[TARGET_COLUMN].astype('float32')

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)

        model = RandomForestRegressor(n_estimators=5, random_state=RANDOM_STATE, n_jobs=1)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        logger.info(f"Model Evaluation - MAE: {mae:.2f}, R2: {r2:.2f}")
        return model, mae, r2
    except Exception as e:
        logger.error(f"Model training error: {str(e)}")
        return None, 0.0, 0.0

def upload_model_to_drive_service_account(model) -> bool:
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build('drive', 'v3', credentials=creds)

        model_bytes = io.BytesIO()
        joblib.dump(model, model_bytes)
        model_bytes.seek(0)

        media = MediaIoBaseUpload(model_bytes, mimetype='application/octet-stream', resumable=True)

        try:
            service.files().get(fileId=DRIVE_FILE_ID).execute()
            request = service.files().update(fileId=DRIVE_FILE_ID, media_body=media)
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    logger.info(f"Upload progress: {int(status.progress() * 100)}%")
            logger.info("Model updated in existing Google Drive file.")
        except HttpError as e:
            if e.resp.status == 404:
                logger.warning("Existing file not found. Creating a new file.")
                file_metadata = {
                    'name': 'weather_model1.pkl',
                    'mimeType': 'application/octet-stream',
                     # If you want to put it in a specific folder, add 'parents': ['YOUR_FOLDER_ID']
                }
                created = service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
                logger.info(f"New model uploaded. File ID: {created.get('id')}")
                # Update DRIVE_FILE_ID if you create a new file and want subsequent runs to update it
                # global DRIVE_FILE_ID
                # DRIVE_FILE_ID = created.get('id')
            else:
                raise

        return True
    except Exception as e:
        logger.error(f"Drive upload failed: {str(e)}", exc_info=True)
        return False

def main():
    logger.info("Starting model training and upload process.")

    # Service account file path is relative to the script
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        logger.error(f"Google Drive service account key file not found at: {SERVICE_ACCOUNT_FILE}")
        logger.error("Please ensure 'mldriveuploader.json' is in the same directory as the script.")
        return

    supabase = initialize_supabase()
    if not supabase:
        return

    try:
        response = supabase.storage.from_(BUCKET_NAME).download(INPUT_FILE)
        df = pd.read_csv(io.BytesIO(response))

        is_valid, msg = validate_dataframe(df)
        if not is_valid:
            logger.error(f"Data validation failed: {msg}")
            return

        model, mae, r2 = train_model(df)
        if model is None:
            logger.error("Model training failed.")
            return

        success = upload_model_to_drive_service_account(model) # No longer need to pass file path explicitly
        if success:
            logger.info("Process completed successfully.")
        else:
            logger.error("Model upload failed.")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
