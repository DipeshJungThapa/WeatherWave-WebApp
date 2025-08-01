import os
import io
import time
import pandas as pd
import requests
from datetime import datetime, timedelta, timezone
from supabase import create_client
import numpy as np

# Supabase credentials (use environment variables in production)
from dotenv import load_dotenv

# Try multiple locations for .env file
env_paths = [
    '.env',  # Root directory (for GitHub Actions)
    os.path.join(os.path.dirname(__file__), '..', '.env'),  # ml/.env (local development)
    os.path.join(os.path.dirname(__file__), '..', '..', '.env')  # Root from ml/data/
]

for path in env_paths:
    if os.path.exists(path):
        load_dotenv(dotenv_path=path)
        print(f"✅ Loaded environment variables from: {path}")
        break
else:
    print("⚠️ No .env file found, trying system environment variables")
    load_dotenv()  # This will load from system environment if available

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Check if required environment variables are loaded
if not SUPABASE_URL or not SUPABASE_KEY:
    print(f"❌ Missing environment variables:")
    print(f"SUPABASE_URL: {'✅' if SUPABASE_URL else '❌'}")
    print(f"SUPABASE_KEY: {'✅' if SUPABASE_KEY else '❌'}")
    raise EnvironmentError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables.")

print("✅ All required environment variables loaded successfully")

BUCKET_NAME = "ml-files"
FILE_PATH = "raw_data.csv"

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Define districts
districts = {
    "Achham": (29.12, 81.30), "Arghakhanchi": (27.95, 83.22), "Baglung": (28.27, 83.61),
    "Baitadi": (29.53, 80.43), "Bajhang": (29.72, 81.25), "Bajura": (29.51, 81.50),
    "Banke": (28.05, 81.62), "Bara": (27.02, 85.05), "Bardiya": (28.30, 81.50),
    "Bhaktapur": (27.67, 85.43), "Bhojpur": (27.17, 87.03), "Chitwan": (27.53, 84.35),
    "Dadeldhura": (29.30, 80.58), "Dailekh": (28.85, 81.70), "Dang": (28.00, 82.30),
    "Darchula": (30.13, 80.58), "Dhading": (27.85, 84.90), "Dhankuta": (26.98, 87.35),
    "Dhanusha": (26.83, 86.03), "Dolakha": (27.66, 86.02), "Dolpa": (29.08, 83.57),
    "Doti": (29.27, 80.93), "East Rukum": (28.63, 82.47), "Gorkha": (28.00, 84.63),
    "Gulmi": (28.08, 83.25), "Humla": (29.96, 81.83), "Ilam": (26.91, 87.92),
    "Jajarkot": (28.70, 82.20), "Jhapa": (26.63, 88.08), "Jumla": (29.27, 82.18),
    "Kailali": (28.70, 80.63), "Kalikot": (29.13, 81.63), "Kanchanpur": (28.83, 80.33),
    "Kapilvastu": (27.55, 83.05), "Kaski": (28.21, 83.99), "Kathmandu": (27.71, 85.32),
    "Kavrepalanchok": (27.63, 85.55), "Khotang": (27.20, 86.80), "Lalitpur": (27.67, 85.32),
    "Lamjung": (28.10, 84.36), "Mahottari": (26.65, 85.90), "Makwanpur": (27.43, 85.03),
    "Manang": (28.65, 84.02), "Morang": (26.67, 87.45), "Mugu": (29.52, 82.10),
    "Mustang": (28.83, 83.83), "Myagdi": (28.38, 83.57), "Nawalpur": (27.70, 84.13),
    "Nuwakot": (27.92, 85.15), "Okhaldhunga": (27.33, 86.50), "Palpa": (27.90, 83.55),
    "Panchthar": (27.13, 87.80), "Parasi": (27.55, 83.70), "Parbat": (28.23, 83.67),
    "Parsa": (27.00, 84.88), "Pyuthan": (28.08, 82.87), "Ramechhap": (27.33, 86.00),
    "Rasuwa": (28.10, 85.27), "Rautahat": (26.93, 85.30), "Rolpa": (28.27, 82.83),
    "Rupandehi": (27.52, 83.45), "Salyan": (28.37, 82.18), "Sankhuwasabha": (27.57, 87.28),
    "Saptari": (26.60, 86.75), "Sarlahi": (26.98, 85.55), "Sindhuli": (27.25, 85.97),
    "Sindhupalchok": (27.85, 85.83), "Siraha": (26.65, 86.20), "Solukhumbu": (27.67, 86.62),
    "Sunsari": (26.62, 87.30), "Surkhet": (28.60, 81.63), "Syangja": (28.08, 83.87),
    "Tanahun": (27.93, 84.25), "Taplejung": (27.35, 87.67), "Terhathum": (27.12, 87.58),
    "Udayapur": (26.85, 86.67), "West Rukum": (28.63, 82.45)
}

# NASA POWER weather parameters
parameters = [
    "PRECTOT", "PS", "QV2M", "RH2M", "T2M", "T2MWET", "T2M_MAX", "T2M_MIN",
    "TS", "WS10M", "WS10M_MAX", "WS10M_MIN", "WS50M", "WS50M_MAX", "WS50M_MIN"
]

# Invalid values that indicate missing/bad data
INVALID_VALUES = [-999, 999, -999.0, 999.0]

def validate_coordinates(lat, lon):
    """Validate latitude and longitude values"""
    if not (-90 <= lat <= 90):
        raise ValueError(f"Invalid latitude: {lat}")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Invalid longitude: {lon}")

def is_valid_weather_record(row):
    """Check if a weather record has valid (non-missing, non-invalid) data for key parameters"""
    # Key parameters that must have valid data
    key_params = ["T2M", "RH2M", "PS"]
    
    valid_count = 0
    for param in key_params:
        if param in row:
            value = row[param]
            # Check if value is not NaN, not None, not empty string, and not in invalid values
            if (pd.notna(value) and 
                value != '' and 
                value is not None and 
                value not in INVALID_VALUES):
                try:
                    # Try to convert to float to ensure it's a valid number
                    float_val = float(value)
                    if not np.isinf(float_val):  # Check for infinity
                        valid_count += 1
                except (ValueError, TypeError):
                    continue
    
    # Require at least 2 out of 3 key parameters to be valid
    return valid_count >= 2

def fetch_weather(district, lat, lon, start, end):
    """Fetch weather data from NASA POWER API with improved error handling"""
    validate_coordinates(lat, lon)
    
    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point?"
        f"start={start}&end={end}&latitude={lat}&longitude={lon}"
        f"&community=ag&parameters={','.join(parameters)}&format=JSON"
    )
    
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            
            json_data = response.json()
            if "properties" not in json_data or "parameter" not in json_data["properties"]:
                print(f"Invalid response structure for {district}")
                continue
                
            data = json_data["properties"]["parameter"]
            
            # Validate that we have temperature data (required parameter)
            if "T2M" not in data or not data["T2M"]:
                print(f"No temperature data for {district}")
                continue
                
            dates = list(data["T2M"].keys())
            
            rows = []
            valid_records = 0
            
            for date in dates:
                row = {"DISTRICT": district, "LAT": lat, "LON": lon, "DATE": date}
                for param in parameters:
                    value = data.get(param, {}).get(date)
                    # Store the raw value, validation will happen later
                    row[param] = value
                
                # Only include records with valid data
                if is_valid_weather_record(row):
                    rows.append(row)
                    valid_records += 1
            
            print(f"✅ Successfully fetched {len(rows)} valid records for {district} (out of {len(dates)} total)")
            return rows
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching {district} (attempt {attempt + 1}/3): {e}")
            if attempt < 2:
                time.sleep(2 ** attempt)  # Exponential backoff
    
    print(f"❌ Failed to fetch {district} after 3 attempts")
    return []

def find_last_valid_date(df):
    """Find the last date with valid (non-missing) data across districts"""
    if df.empty:
        return None
    
    # Convert DATE to datetime for comparison, handling both string and numeric formats
    df_temp = df.copy()
    
    # Ensure DATE is string first
    df_temp["DATE"] = df_temp["DATE"].astype(str)
    
    # Convert to datetime
    df_temp["DATE"] = pd.to_datetime(df_temp["DATE"], format="%Y%m%d", errors="coerce")
    
    # Remove rows with invalid dates
    df_temp = df_temp.dropna(subset=["DATE"])
    
    if df_temp.empty:
        return None
    
    # Check each date from most recent to oldest
    dates_sorted = sorted(df_temp["DATE"].unique(), reverse=True)
    
    print(f"🔍 Checking {len(dates_sorted)} dates for valid data...")
    
    for date in dates_sorted:
        date_data = df_temp[df_temp["DATE"] == date]
        
        # Check if this date has valid data for districts
        valid_districts = 0
        total_districts = len(date_data)
        
        for _, row in date_data.iterrows():
            if is_valid_weather_record(row):
                valid_districts += 1
        
        # If at least 70% of districts have valid data for this date, consider it valid
        if total_districts > 0:
            valid_percentage = (valid_districts / total_districts) * 100
            
            if valid_percentage >= 70:
                print(f"📅 Last valid date found: {date.strftime('%Y%m%d')} ({valid_districts}/{total_districts} districts = {valid_percentage:.1f}% valid)")
                return date
            else:
                print(f"📊 Date {date.strftime('%Y%m%d')}: {valid_districts}/{total_districts} districts = {valid_percentage:.1f}% valid (below 70% threshold)")
    
    print("⚠️ No dates with sufficient valid data found (70% threshold)")
    return None

def get_existing_data():
    """Load existing CSV from Supabase with improved error handling"""
    try:
        response = supabase.storage.from_(BUCKET_NAME).download(FILE_PATH)
        df = pd.read_csv(io.BytesIO(response))
        
        # Ensure DATE is in string format for consistency
        df["DATE"] = df["DATE"].astype(str)
        
        print(f"✅ Loaded {len(df)} existing records")
        print(f"📊 Districts in data: {df['DISTRICT'].nunique()}")
        print(f"📊 Date range: {df['DATE'].min()} to {df['DATE'].max()}")
        
        # Show sample of data quality
        sample_row = df.iloc[0] if not df.empty else None
        if sample_row is not None:
            valid = is_valid_weather_record(sample_row)
            print(f"📊 Sample record valid: {valid}")
        
        return df
        
    except Exception as e:
        print(f"ℹ️ No existing data found or error occurred: {e}")
        return pd.DataFrame()

def upload_to_supabase(df):
    """Upload CSV to Supabase with improved error handling"""
    if df is None or df.empty:
        raise ValueError("Invalid DataFrame for upload")
    
    # Ensure DATE is in YYYYMMDD string format
    df_copy = df.copy()
    df_copy["DATE"] = df_copy["DATE"].astype(str)
    
    csv_buffer = io.StringIO()
    df_copy.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode("utf-8")
    
    try:
        # Check if file exists and remove it
        files = supabase.storage.from_(BUCKET_NAME).list()
        if any(file['name'] == FILE_PATH for file in files):
            supabase.storage.from_(BUCKET_NAME).remove([FILE_PATH])
            print(f"🗑️ Removed existing file {FILE_PATH}")
        
        supabase.storage.from_(BUCKET_NAME).upload(
            FILE_PATH,
            csv_bytes,
            {"content-type": "text/csv"}
        )
        print(f"✅ Successfully uploaded {len(df)} records to Supabase")
        
    except Exception as e:
        print(f"❌ Failed to upload to Supabase: {e}")
        raise

def main():
    """Main execution function with improved logic for valid data detection"""
    print("🌤️ Starting weather data fetch with valid data detection...")
    
    df_existing = get_existing_data()
    current_date = datetime.now(timezone.utc)
    
    if not df_existing.empty:
        # Find the last date with valid data
        last_valid_date = find_last_valid_date(df_existing)
        
        if last_valid_date:
            # Check if we need to update
            days_since_last_valid = (current_date.date() - last_valid_date.date()).days
            
            if days_since_last_valid <= 1:
                print("📅 Data is up to date with valid records")
                return
            
            # Start from the day after the last valid date
            start_date = (last_valid_date + timedelta(days=1)).strftime("%Y%m%d")
            print(f"📊 Updating from last valid date: {last_valid_date.strftime('%Y%m%d')}")
        else:
            # No valid data found, get the latest date and start from there
            if 'DATE' in df_existing.columns:
                df_existing['DATE'] = df_existing['DATE'].astype(str)
                latest_date_str = df_existing['DATE'].max()
                try:
                    latest_date = datetime.strptime(latest_date_str, "%Y%m%d")
                    start_date = (latest_date + timedelta(days=1)).strftime("%Y%m%d")
                    print(f"⚠️ No valid data found, but continuing from latest date: {latest_date_str}")
                except:
                    start_date = "20100101"
                    print("⚠️ Could not parse latest date, starting from 2010")
            else:
                start_date = "20100101"
                print("⚠️ No DATE column found, starting from 2010")
    else:
        start_date = "20100101"  # Start from 2010 if no existing data
        print("📊 No existing data, starting from 2010")
    
    end_date = (current_date - timedelta(days=1)).strftime("%Y%m%d")
    
    if start_date > end_date:
        print("📅 Data is already up to date")
        return
    
    print(f"📊 Fetching data from {start_date} to {end_date}")
    
    all_rows = []
    total_districts = len(districts)
    successful_fetches = 0
    
    for i, (district, (lat, lon)) in enumerate(districts.items(), 1):
        print(f"🌍 [{i}/{total_districts}] Fetching {district}...")
        
        try:
            new_rows = fetch_weather(district, lat, lon, start_date, end_date)
            if new_rows:
                all_rows.extend(new_rows)
                successful_fetches += 1
            
            # Rate limiting to be respectful to the API
            if i < total_districts:
                time.sleep(1)
                
        except Exception as e:
            print(f"❌ Error processing {district}: {e}")
            continue
    
    if not all_rows:
        print("ℹ️ No new valid data to process")
        return
    
    print(f"📊 Processing {len(all_rows)} new valid records from {successful_fetches} districts...")
    
    # Create DataFrame with proper formatting
    df_new = pd.DataFrame(all_rows)
    df_new["DATE"] = df_new["DATE"].astype(str)
    
    # Combine with existing data
    if not df_existing.empty:
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined = df_combined.drop_duplicates(subset=["DISTRICT", "DATE"], keep="last")
    else:
        df_combined = df_new
    
    # Sort by district and date
    df_combined = df_combined.sort_values(["DISTRICT", "DATE"]).reset_index(drop=True)
    
    # Final validation - count valid records
    valid_count = sum(1 for _, row in df_combined.iterrows() if is_valid_weather_record(row))
    
    print(f"📊 Final dataset: {len(df_combined)} total records, {valid_count} with valid data ({(valid_count/len(df_combined)*100):.1f}%)")
    
    upload_to_supabase(df_combined)
    print(f"✅ Successfully processed and uploaded {len(df_combined)} total records")

if __name__ == "__main__":
    main()