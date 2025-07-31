import os
import io
import time
import pandas as pd
import requests
from datetime import datetime, timedelta, timezone
from supabase import create_client
import numpy as np

# Supabase credentials from environment variables (set in GitHub Actions secrets)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "ml-files"
FILE_PATH = "raw_data.csv"

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables.")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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

parameters = [
    "PRECTOT", "PS", "QV2M", "RH2M", "T2M", "T2MWET", "T2M_MAX", "T2M_MIN",
    "TS", "WS10M", "WS10M_MAX", "WS10M_MIN", "WS50M", "WS50M_MAX", "WS50M_MIN"
]

INVALID_VALUES = [-999, 999, -999.0, 999.0]

def validate_coordinates(lat, lon):
    if not (-90 <= lat <= 90):
        raise ValueError(f"Invalid latitude: {lat}")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Invalid longitude: {lon}")

def is_valid_weather_record(row):
    key_params = ["T2M", "RH2M", "PS"]
    valid_count = 0
    for param in key_params:
        if param in row:
            value = row[param]
            if (pd.notna(value) and value != '' and value is not None and value not in INVALID_VALUES):
                try:
                    float_val = float(value)
                    if not np.isinf(float_val):
                        valid_count += 1
                except (ValueError, TypeError):
                    continue
    return valid_count >= 2

def fetch_weather(district, lat, lon, start, end):
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
                print(f"[{district}] Invalid response structure")
                continue
            data = json_data["properties"]["parameter"]
            if "T2M" not in data or not data["T2M"]:
                print(f"[{district}] No temperature data")
                continue
            dates = list(data["T2M"].keys())
            rows = []
            for date in dates:
                row = {"DISTRICT": district, "LAT": lat, "LON": lon, "DATE": date}
                for param in parameters:
                    row[param] = data.get(param, {}).get(date)
                if is_valid_weather_record(row):
                    rows.append(row)
            print(f"[{district}] Fetched {len(rows)} valid records out of {len(dates)}")
            return rows
        except requests.exceptions.RequestException as e:
            print(f"[{district}] Fetch error attempt {attempt + 1}/3: {e}")
            if attempt < 2:
                time.sleep(2 ** attempt)
    print(f"[{district}] Failed to fetch after 3 attempts")
    return []

def find_last_valid_date(df):
    if df.empty:
        return None
    df_temp = df.copy()
    df_temp["DATE"] = pd.to_datetime(df_temp["DATE"].astype(str), format="%Y%m%d", errors="coerce")
    df_temp = df_temp.dropna(subset=["DATE"])
    if df_temp.empty:
        return None
    dates_sorted = sorted(df_temp["DATE"].unique(), reverse=True)
    print(f"Checking {len(dates_sorted)} dates for valid data...")
    for date in dates_sorted:
        date_data = df_temp[df_temp["DATE"] == date]
        total = len(date_data)
        valid = sum(is_valid_weather_record(row) for _, row in date_data.iterrows())
        if total > 0:
            percent = (valid / total) * 100
            if percent >= 70:
                print(f"Last valid date: {date.strftime('%Y%m%d')} ({valid}/{total} districts = {percent:.1f}%)")
                return date
            else:
                print(f"Date {date.strftime('%Y%m%d')}: {valid}/{total} districts = {percent:.1f}% valid (<70%)")
    print("No sufficient valid data found (70% threshold).")
    return None

def get_existing_data():
    try:
        response = supabase.storage.from_(BUCKET_NAME).download(FILE_PATH)
        df = pd.read_csv(io.BytesIO(response))
        df["DATE"] = df["DATE"].astype(str)
        print(f"Loaded {len(df)} records, {df['DISTRICT'].nunique()} districts, dates {df['DATE'].min()} to {df['DATE'].max()}")
        return df
    except Exception as e:
        print(f"No existing data or error: {e}")
        return pd.DataFrame()

def upload_to_supabase(df):
    if df is None or df.empty:
        raise ValueError("Empty DataFrame cannot be uploaded")
    df_copy = df.copy()
    df_copy["DATE"] = df_copy["DATE"].astype(str)
    csv_buffer = io.StringIO()
    df_copy.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode("utf-8")
    try:
        files = supabase.storage.from_(BUCKET_NAME).list()
        if any(f['name'] == FILE_PATH for f in files):
            supabase.storage.from_(BUCKET_NAME).remove([FILE_PATH])
            print(f"Removed existing file {FILE_PATH}")
        supabase.storage.from_(BUCKET_NAME).upload(FILE_PATH, csv_bytes, {"content-type": "text/csv"})
        print(f"Uploaded {len(df)} records to Supabase")
    except Exception as e:
        print(f"Upload failed: {e}")
        raise

def main():
    print("Starting weather data fetch...")
    df_existing = get_existing_data()
    now = datetime.now(timezone.utc)

    if not df_existing.empty:
        last_valid = find_last_valid_date(df_existing)
        if last_valid:
            days_diff = (now.date() - last_valid.date()).days
            if days_diff <= 1:
                print("Data is up to date.")
                return
            start_date = (last_valid + timedelta(days=1)).strftime("%Y%m%d")
            print(f"Updating from last valid date: {start_date}")
        else:
            try:
                latest_str = df_existing["DATE"].max()
                latest_date = datetime.strptime(latest_str, "%Y%m%d")
                start_date = (latest_date + timedelta(days=1)).strftime("%Y%m%d")
                print(f"No valid data found; continuing from latest date: {start_date}")
            except Exception:
                start_date = "20100101"
                print("Could not parse latest date; starting from 20100101")
    else:
        start_date = "20100101"
        print("No existing data; starting from 20100101")

    end_date = (now - timedelta(days=1)).strftime("%Y%m%d")

    if start_date > end_date:
        print("Data already up to date.")
        return

    print(f"Fetching data from {start_date} to {end_date}...")

    all_rows = []
    total = len(districts)
    success_count = 0

    for i, (district, (lat, lon)) in enumerate(districts.items(), 1):
        print(f"[{i}/{total}] Fetching {district}...")
        try:
            rows = fetch_weather(district, lat, lon, start_date, end_date)
            if rows:
                all_rows.extend(rows)
                success_count += 1
            if i < total:
                time.sleep(1)  # rate limiting
        except Exception as e:
            print(f"Error fetching {district}: {e}")
            continue

    if not all_rows:
        print("No new valid data fetched.")
        return

    print(f"Processing {len(all_rows)} new records from {success_count} districts...")

    df_new = pd.DataFrame(all_rows)
    df_new["DATE"] = df_new["DATE"].astype(str)

    if not df_existing.empty:
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined = df_combined.drop_duplicates(subset=["DISTRICT", "DATE"], keep="last")
    else:
        df_combined = df_new

    df_combined = df_combined.sort_values(["DISTRICT", "DATE"]).reset_index(drop=True)

    valid_count = sum(is_valid_weather_record(row) for _, row in df_combined.iterrows())
    print(f"Final dataset: {len(df_combined)} records, {valid_count} valid ({valid_count / len(df_combined) * 100:.1f}%)")

    upload_to_supabase(df_combined)
    print("Upload complete.")

if __name__ == "__main__":
    main()
