import requests
import pandas as pd
import time
from datetime import datetime, timedelta, timezone
import os

# All 77 districts with coordinates
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

# NASA POWER parameters to fetch
parameters = [
    "PRECTOT", "PS", "QV2M", "RH2M", "T2M", "T2MWET", "T2M_MAX", "T2M_MIN",
    "TS", "WS10M", "WS10M_MAX", "WS10M_MIN", "WS50M", "WS50M_MAX", "WS50M_MIN"
]

def fetch_data(district, lat, lon, start, end):
    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point?"
        f"start={start}&end={end}&latitude={lat}&longitude={lon}"
        f"&community=ag&parameters={','.join(parameters)}&format=JSON"
    )
    try:
        response = requests.get(url, timeout=60)
        if response.status_code != 200:
            print(f"Failed: {district} ({start} to {end})")
            return []

        json_data = response.json()
        data = json_data.get("properties", {}).get("parameter", {})
        dates = list(data.get("T2M", {}).keys())

        records = []
        for date in dates:
            record = {"DISTRICT": district, "LAT": lat, "LON": lon, "DATE": date}
            for param in parameters:
                record[param] = data.get(param, {}).get(date)
            records.append(record)
        return records
    except Exception as e:
        print(f"Error fetching {district}: {e}")
        return []

def get_last_date(csv_file):
    if not os.path.exists(csv_file):
        return None
    df = pd.read_csv(csv_file)
    if df.empty or 'DATE' not in df.columns:
        return None
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d', errors='coerce')
    return df['DATE'].max()

def main():
    csv_file = "raw_data.csv"
    last_date = get_last_date(csv_file)
    start_date = (last_date + timedelta(days=1)).strftime("%Y%m%d") if last_date else "20100101"
    end_date = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y%m%d")

    if last_date and start_date > end_date:
        print("✅ Data already up to date.")
        return

    all_data = []
    for district, (lat, lon) in districts.items():
        print(f"Fetching {district}...")
        all_data.extend(fetch_data(district, lat, lon, start_date, end_date))
        time.sleep(1)

    if all_data:
        df_new = pd.DataFrame(all_data)
        if os.path.exists(csv_file):
            df_existing = pd.read_csv(csv_file)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.drop_duplicates(subset=["DISTRICT", "DATE"], keep="last", inplace=True)
        else:
            df_combined = df_new
        df_combined.to_csv(csv_file, index=False)
        print("✅ Weather data saved to", csv_file)
    else:
        print("⚠️ No new data was fetched.")

if __name__ == "__main__":
    main()
