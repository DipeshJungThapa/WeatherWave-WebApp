from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import requests
from dotenv import load_dotenv
import os
import datetime
import pandas as pd
import io

# Define a manual dictionary for districts with their latitude and longitude
DISTRICT_GEOLOCATION_MAP = {
    "Achham": {"latitude": 29.1200, "longitude": 81.3000},
    "Arghakhanchi": {"latitude": 27.9500, "longitude": 83.2000},
    "Baglung": {"latitude": 28.2667, "longitude": 83.6167},
    "Baitadi": {"latitude": 29.5167, "longitude": 80.5500},
    "Bajhang": {"latitude": 29.8333, "longitude": 81.2500},
    "Bajura": {"latitude": 29.4000, "longitude": 81.5000},
    "Banke": {"latitude": 28.0500, "longitude": 81.6167},
    "Bara": {"latitude": 27.2167, "longitude": 85.0167},
    "Bardiya": {"latitude": 28.3000, "longitude": 81.4167},
    "Bhaktapur": {"latitude": 27.6710, "longitude": 85.4298},
    "Bhojpur": {"latitude": 27.1700, "longitude": 87.0500},
    "Chitwan": {"latitude": 27.5291, "longitude": 84.3542},
    "Dadeldhura": {"latitude": 29.3000, "longitude": 80.5833},
    "Dailekh": {"latitude": 28.8442, "longitude": 81.7101},
    "Dang": {"latitude": 28.0500, "longitude": 82.3000},
    "Darchula": {"latitude": 30.1500, "longitude": 80.5833},
    "Dhading": {"latitude": 27.9000, "longitude": 84.9167},
    "Dhankuta": {"latitude": 26.9833, "longitude": 87.3500},
    "Dhanusha": {"latitude": 26.8167, "longitude": 86.0333},
    "Dolakha": {"latitude": 27.6667, "longitude": 86.0500},
    "Dolpa": {"latitude": 29.0694, "longitude": 83.5800},
    "Doti": {"latitude": 29.2667, "longitude": 80.9333},
    "Eastern Rukum": {"latitude": 28.6260, "longitude": 83.3604},
    "Gorkha": {"latitude": 28.0000, "longitude": 84.6333},
    "Gulmi": {"latitude": 28.0833, "longitude": 83.2500},
    "Humla": {"latitude": 29.9667, "longitude": 81.8333},
    "Ilam": {"latitude": 26.9110, "longitude": 87.9286},
    "Jajarkot": {"latitude": 28.7000, "longitude": 82.1833},
    "Jhapa": {"latitude": 26.5456, "longitude": 87.9036},
    "Jumla": {"latitude": 29.2806, "longitude": 82.3033},
    "Kailali": {"latitude": 28.5300, "longitude": 80.6200},
    "Kalikot": {"latitude": 29.1333, "longitude": 82.0000},
    "Kanchanpur": {"latitude": 28.8333, "longitude": 80.3333},
    "Kapilvastu": {"latitude": 27.5500, "longitude": 83.0500},
    "Kaski": {"latitude": 28.2333, "longitude": 83.9833},
    "Kathmandu": {"latitude": 27.7172, "longitude": 85.3240},
    "Kavrepalanchok": {"latitude": 27.6333, "longitude": 85.5333},
    "Khotang": {"latitude": 27.2038, "longitude": 86.7893},
    "Lalitpur": {"latitude": 27.6766, "longitude": 85.3188},
    "Lamjung": {"latitude": 28.2667, "longitude": 84.3667},
    "Mahottari": {"latitude": 26.6500, "longitude": 85.8167},
    "Makwanpur": {"latitude": 27.4333, "longitude": 85.0333},
    "Manang": {"latitude": 28.6667, "longitude": 84.0167},
    "Morang": {"latitude": 26.6667, "longitude": 87.5000},
    "Mugu": {"latitude": 29.6167, "longitude": 82.3833},
    "Mustang": {"latitude": 28.9985, "longitude": 83.8963},
    "Myagdi": {"latitude": 28.3500, "longitude": 83.5667},
    "Nawalpur": {"latitude": 27.6928, "longitude": 84.1272},
    "Nuwakot": {"latitude": 27.8700, "longitude": 85.1400},
    "Okhaldhunga": {"latitude": 27.3167, "longitude": 86.5000},
    "Palpa": {"latitude": 27.8667, "longitude": 83.5500},
    "Panchthar": {"latitude": 27.1167, "longitude": 87.9333},
    "Parbat": {"latitude": 28.2333, "longitude": 83.7000},
    "Parsa": {"latitude": 27.0000, "longitude": 84.8667},
    "Pyuthan": {"latitude": 28.0833, "longitude": 82.8500},
    "Ramechhap": {"latitude": 27.3833, "longitude": 86.0833},
    "Rasuwa": {"latitude": 28.0500, "longitude": 85.3333},
    "Rautahat": {"latitude": 26.9333, "longitude": 85.3000},
    "Rolpa": {"latitude": 28.3500, "longitude": 82.8667},
    "Rupandehi": {"latitude": 27.6333, "longitude": 83.5500},
    "Salyan": {"latitude": 28.3833, "longitude": 82.1500},
    "Sankhuwasabha": {"latitude": 27.5833, "longitude": 87.3000},
    "Saptari": {"latitude": 26.6167, "longitude": 86.7500},
    "Sarlahi": {"latitude": 26.9833, "longitude": 85.5667},
    "Sindhuli": {"latitude": 27.2500, "longitude": 85.9167},
    "Sindhupalchok": {"latitude": 27.8014, "longitude": 85.7006},
    "Siraha": {"latitude": 26.6500, "longitude": 86.2000},
    "Solukhumbu": {"latitude": 27.6690, "longitude": 86.7140},
    "Sunsari": {"latitude": 26.6167, "longitude": 87.2500},
    "Surkhet": {"latitude": 28.6000, "longitude": 81.6333},
    "Syangja": {"latitude": 28.0069, "longitude": 83.8622},
    "Tanahun": {"latitude": 27.9316, "longitude": 84.2570},
    "Taplejung": {"latitude": 27.3543, "longitude": 87.6792},
    "Terhathum": {"latitude": 27.0000, "longitude": 87.6000},
    "Udayapur": {"latitude": 26.7911, "longitude": 86.6913},
    "Western Rukum": {"latitude": 28.6274, "longitude": 82.3425}
}

# --- Helper functions ---
from .models import Weather
from .serializers import WeatherSerializer

# Helper: Get geolocation from IP as fallback
def get_geolocation():
    url = "https://ipinfo.io/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        loc = data.get('loc', '').split(',')
        latitude = loc[0] if len(loc) == 2 else None
        longitude = loc[1] if len(loc) == 2 else None
        return {
            "ip": data.get('ip'),
            "city": data.get('city', ''),
            "region": data.get('region'),
            "country": data.get('country'),
            "latitude": latitude,
            "longitude": longitude,
        }
    except requests.RequestException:
        return None

# Helper: Get lat/lon from city name using OpenWeatherMap Geocoding API
def get_lat_lon_from_city(city):
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        return None, None
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data and len(data) > 0:
            return str(data[0]['lat']), str(data[0]['lon'])
        else:
            return None, None
    except Exception:
        return None, None

def get_weather(lat, lon, api_key):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "city_name": data.get('name'),
            "temp": data['main']['temp'],
            "description": data['weather'][0]['description'],
            "humidity": data['main']['humidity'],
            "wind_speed": data['wind']['speed'],
        }
    except requests.RequestException:
        return None

def compute_pm25_aqi(concentration):
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500),
    ]
    for c_lo, c_hi, i_lo, i_hi in breakpoints:
        if c_lo <= concentration <= c_hi:
            return round(((i_hi - i_lo) / (c_hi - c_lo)) * (concentration - c_lo) + i_lo)
    return None  # Out of range

@api_view(['GET'])
@permission_classes([AllowAny])
def get_current_weather(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')
    city = request.query_params.get('city')
    API_KEY = os.getenv('OPENWEATHER_API_KEY')

    if not API_KEY:
        return Response({"error": "OpenWeather API key not configured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if lat and lon:
        weather = get_weather(lat, lon, API_KEY)
        city_name = city if city else (weather.get("city_name") if weather else None)
    elif city:
        lat, lon = get_lat_lon_from_city(city)
        if not lat or not lon:
            # Fallback to manual map
            geo = DISTRICT_GEOLOCATION_MAP.get(city)
            if geo:
                lat, lon = geo['latitude'], geo['longitude']
        if lat and lon:
            weather = get_weather(lat, lon, API_KEY)
            city_name = city
        else:
            weather = None
            city_name = city
    else:
        geo = get_geolocation()
        lat = geo.get("latitude") if geo else None
        lon = geo.get("longitude") if geo else None
        weather = get_weather(lat, lon, API_KEY) if lat and lon else None
        city_name = geo.get("city") if geo else None

    if not weather:
        return Response({"error": "Could not fetch weather data"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "city": city_name,
        "temp": weather["temp"] if weather else None,
        "humidity": weather["humidity"] if weather else None,
        "description": weather["description"] if weather else None,
        "wind_speed": weather["wind_speed"] if weather else None,
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_aqi(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')
    city = request.query_params.get('city')
    API_KEY = os.getenv('WEATHER_API_KEY')

    if not API_KEY:
        return Response({"error": "Weather API key not configured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if lat and lon:
        query_lat, query_lon = lat, lon
    elif city:
        query_lat, query_lon = get_lat_lon_from_city(city)
        if not query_lat or not query_lon:
            # Fallback to manual map
            geo = DISTRICT_GEOLOCATION_MAP.get(city)
            if geo:
                query_lat, query_lon = geo['latitude'], geo['longitude']
    else:
        geo = get_geolocation()
        query_lat = geo.get("latitude") if geo else None
        query_lon = geo.get("longitude") if geo else None

    if not query_lat or not query_lon:
        return Response({"error": "Could not determine location"}, status=status.HTTP_400_BAD_REQUEST)

    url = (
        f"http://api.weatherapi.com/v1/current.json?"
        f"key={API_KEY}&q={query_lat},{query_lon}&aqi=yes"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        air_quality = data.get("current", {}).get("air_quality", {})
        pm25 = air_quality.get("pm2_5")

        if pm25 is None:
            return Response({"error": "PM2.5 data not available"}, status=500)

        real_aqi = compute_pm25_aqi(pm25)

        return Response({
            "AQI_Value": real_aqi,
        })
    except requests.RequestException as e:
        return Response({"error": "Error fetching AQI data", "details": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_weather_history(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')
    city = request.query_params.get('city')
    API_KEY = os.getenv('WEATHER_API_KEY')

    if not API_KEY:
        return Response({"error": "Weather API key not configured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if lat and lon:
        query_lat, query_lon = lat, lon
    elif city:
        query_lat, query_lon = get_lat_lon_from_city(city)
    else:
        geo = get_geolocation()
        query_lat = geo.get("latitude") if geo else None
        query_lon = geo.get("longitude") if geo else None

    if not query_lat or not query_lon:
        return Response({"error": "Could not determine location"}, status=status.HTTP_400_BAD_REQUEST)

    history = []
    for i in range(1, 6):
        date = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        history_url = (
            f"http://api.weatherapi.com/v1/history.json?"
            f"key={API_KEY}&q={query_lat},{query_lon}&dt={date}&aqi=yes"
        )
        try:
            resp = requests.get(history_url)
            resp.raise_for_status()
            hist_data = resp.json()
            day_data = hist_data.get('forecast', {}).get('forecastday', [{}])[0]
            aqi_data = day_data.get('day', {}).get('air_quality', {})
            history.append({
                "date": date,
                "Weather": {
                    "avg_temp": day_data.get('day', {}).get('avgtemp_c'),
                    "max_temp": day_data.get('day', {}).get('maxtemp_c'),
                    "min_temp": day_data.get('day', {}).get('mintemp_c'),
                }
            })
        except requests.RequestException as e:
            history.append({"date": date, "error": str(e)})

    return Response({"history": history})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_weather_forecast(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')
    city = request.query_params.get('city')
    API_KEY = os.getenv('OPENWEATHER_API_KEY')

    if not API_KEY:
        return Response({"error": "OpenWeather API key not configured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if lat and lon:
        query_lat, query_lon = lat, lon
    elif city:
        query_lat, query_lon = get_lat_lon_from_city(city)
        if not query_lat or not query_lon:
            # Fallback to manual map
            geo = DISTRICT_GEOLOCATION_MAP.get(city)
            if geo:
                query_lat, query_lon = geo['latitude'], geo['longitude']
    else:
        geo = get_geolocation()
        query_lat = geo.get("latitude") if geo else None
        query_lon = geo.get("longitude") if geo else None

    if not query_lat or not query_lon:
        return Response({"error": "Could not determine location"}, status=status.HTTP_400_BAD_REQUEST)

    forecast_url = (
        f"http://api.openweathermap.org/data/2.5/forecast?"
        f"lat={query_lat}&lon={query_lon}&appid={API_KEY}&units=metric"
    )
    forecast_data = []
    try:
        resp = requests.get(forecast_url)
        resp.raise_for_status()
        forecast_json = resp.json()
        # Group by date and get min/max/avg for each day
        daily = {}
        for entry in forecast_json.get('list', []):
            date = entry['dt_txt'].split(' ')[0]
            temp = entry['main']['temp']
            if date not in daily:
                daily[date] = {"temps": []}
            daily[date]["temps"].append(temp)
        # Only keep the next 5 days
        for i, (date, vals) in enumerate(daily.items()):
            if i >= 5:
                break
            temps = vals["temps"]
            forecast_data.append({
                "date": date,
                "Weather": {
                    "avg_temp": sum(temps) / len(temps),
                    "max_temp": max(temps),
                    "min_temp": min(temps),
                }
            })
    except requests.RequestException as e:
        return Response({"error": f"Error fetching forecast data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        "forecast": forecast_data
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_alert(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')
    city = request.query_params.get('city')
    API_KEY = os.getenv('WEATHERBIT_API_KEY') 

    if not API_KEY:
        return Response({"error": "Weatherbit API key not configured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if lat and lon:
        query_lat, query_lon = lat, lon
    elif city:
        query_lat, query_lon = get_lat_lon_from_city(city)
        if not query_lat or not query_lon:
            # Fallback to manual map
            geo = DISTRICT_GEOLOCATION_MAP.get(city)
            if geo:
                query_lat, query_lon = geo['latitude'], geo['longitude']
    else:
        geo = get_geolocation()
        query_lat = geo.get("latitude") if geo else None
        query_lon = geo.get("longitude") if geo else None

    if not query_lat or not query_lon:
        return Response({"error": "Could not determine location"}, status=status.HTTP_400_BAD_REQUEST)

    alert_url = (
        f"https://api.weatherbit.io/v2.0/alerts?lat={query_lat}&lon={query_lon}&key={API_KEY}"
    )

    try:
        response = requests.get(alert_url)
        response.raise_for_status()
        data = response.json()
        alerts = data.get('alerts', [])
        if not alerts:
            return Response({"message": "No weather alerts at this time."})
        return Response({"alerts": alerts})
    except requests.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from supabase import create_client
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "ml-files"
PREDICTION_FILE = "predictions.csv"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@api_view(['POST'])
@permission_classes([AllowAny])
def predict_geo(request):
    lat = request.data.get('lat')
    lon = request.data.get('lon')

    if not lat or not lon:
        return Response({"error": "Latitude and Longitude are required."}, status=400)

    try:
        lat = float(lat)
        lon = float(lon)

        # Resolve nearest district from lat/lon
        min_dist = float('inf')
        closest_district = None
        for district, info in DISTRICT_GEOLOCATION_MAP.items():
            dist = ((lat - info['latitude'])**2 + (lon - info['longitude'])**2)**0.5
            if dist < min_dist:
                min_dist = dist
                closest_district = district

        if closest_district is None:
            return Response({"error": "Could not resolve coordinates to a district."}, status=404)

        # Load predictions.csv from Supabase
        file_bytes = supabase.storage.from_(BUCKET_NAME).download(PREDICTION_FILE)
        df = pd.read_csv(io.BytesIO(file_bytes))
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Filter by closest_district
        latest_data = df[df['District'] == closest_district]
        if latest_data.empty:
            return Response({"error": f"No prediction found for district: {closest_district}"}, status=404)

        latest_row = latest_data.sort_values(by='Date', ascending=False).iloc[0]

        return Response({
            "resolved_district": closest_district,
            "predicted_temp": round(latest_row['predicted_Temp_2m_tomorrow'], 2)
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def predict_city(request):
    city = request.data.get('city')
    if not city:
        return Response({"error": "City name is required."}, status=400)

    try:
        if city not in DISTRICT_GEOLOCATION_MAP:
            return Response({"error": f"City '{city}' not found in district map."}, status=404)

        # Load predictions.csv from Supabase
        file_bytes = supabase.storage.from_(BUCKET_NAME).download(PREDICTION_FILE)
        df = pd.read_csv(io.BytesIO(file_bytes))
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Filter by city
        city_data = df[df['District'] == city]
        if city_data.empty:
            return Response({"error": f"No prediction data found for city: {city}"}, status=404)

        latest = city_data.sort_values(by='Date', ascending=False).iloc[0]

        return Response({
            "city": city,
            "predicted_temp": round(latest['predicted_Temp_2m_tomorrow'], 2)
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def get_current_weather_default(request):
    city = request.data.get('city')
    if not city:
        return Response({'error': 'City field is required in the request body.'}, status=400)
    
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        return Response({'error': 'OpenWeather API key not configured'}, status=500)
        
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            return Response({'error': data.get('message', 'Failed to fetch weather data.')}, status=response.status_code)
        
        weather = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
        }
        return Response(weather)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_weather_news(request):
    """
    Returns weather-related news for Nepal.
    Since we don't have a real news API, this returns mock data.
    """
    from datetime import datetime, timedelta
    
    # Mock weather news data for Nepal
    mock_news = [
        {
            "id": 1,
            "title": "Nepal Weather Update: Monsoon Season Continues",
            "summary": "Heavy rainfall expected in eastern regions with chances of flooding in low-lying areas. The Department of Hydrology and Meteorology has issued warnings for several districts.",
            "url": "#",
            "published_at": datetime.now().isoformat(),
            "source": "Nepal Weather Service"
        },
        {
            "id": 2,
            "title": "Air Quality Alert for Kathmandu Valley",
            "summary": "PM2.5 levels remain elevated due to dust and vehicle emissions. Citizens advised to limit outdoor activities and use masks when going outside.",
            "url": "#",
            "published_at": (datetime.now() - timedelta(hours=1)).isoformat(),
            "source": "Department of Environment"
        },
        {
            "id": 3,
            "title": "Temperature Records Broken in Terai Region",
            "summary": "Several districts in the Terai region recorded temperatures above 40°C, breaking previous records. Heat wave warnings issued for affected areas.",
            "url": "#",
            "published_at": (datetime.now() - timedelta(hours=2)).isoformat(),
            "source": "Meteorological Forecasting Division"
        },
        {
            "id": 4,
            "title": "Flash Flood Warning for Hill Districts",
            "summary": "Meteorological department warns of possible flash floods in hill districts due to continuous rainfall. Residents near rivers advised to stay alert.",
            "url": "#",
            "published_at": (datetime.now() - timedelta(hours=4)).isoformat(),
            "source": "Department of Hydrology"
        },
        {
            "id": 5,
            "title": "Drought Conditions in Western Nepal",
            "summary": "Western districts experiencing below-normal rainfall this season. Agricultural activities may be affected if the pattern continues.",
            "url": "#",
            "published_at": (datetime.now() - timedelta(hours=6)).isoformat(),
            "source": "Nepal Agricultural Research Council"
        }
    ]
    
    return Response(mock_news)