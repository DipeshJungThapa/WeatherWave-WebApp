from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import os
import datetime
from dotenv import load_dotenv
from django.conf import settings
import joblib

load_dotenv()

# ------------------ Helper Functions (unchanged, but ensure they are present) ------------------

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
            "city": data.get('city'),
            "region": data.get('region'),
            "country": data.get('country'),
            "latitude": latitude,
            "longitude": longitude,
        }
    except requests.RequestException:
        return None

def get_weather(lat, lon, api_key):
    # OpenWeatherMap API for current weather
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={api_key}&units=metric" # units=metric gives Celsius
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Extracting relevant data for the 21 features
        # Some fields might not always be present (e.g., 'rain', 'snow', 'gust')
        
        # Precip (rain/snow volume for the last 1 hour, in mm)
        precip = 0.0
        if 'rain' in data and '1h' in data['rain']:
            precip += data['rain']['1h']
        if 'snow' in data and '1h' in data['snow']:
            precip += data['snow']['1h']

        # Wind Gust (proxy for MaxWindSpeed_10m)
        wind_gust = data.get('wind', {}).get('gust', data.get('wind', {}).get('speed', 0.0)) # use speed if gust not available

        return {
            "temp": data['main']['temp'],
            "description": data['weather'][0]['description'],
            "humidity": data['main']['humidity'], # This is Humidity_2m and RH_2m
            "wind_speed": data['wind']['speed'], # This is WindSpeed_10m
            "pressure": data['main']['pressure'], # This is Pressure
            "temp_max": data['main'].get('temp_max'), # MaxTemp_2m (proxy)
            "temp_min": data['main'].get('temp_min'), # MinTemp_2m (proxy)
            "precip": precip, # Precip
            "wind_gust": wind_gust, # MaxWindSpeed_10m (proxy)
            # Other features like WetBulbTemp_2m, EarthSkinTemp, WindSpeed_50m are not directly from here
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
    return None

# NEW HELPER: For predict_city to get lat/lon from city name
def get_lat_lon_from_city(city_name, api_key):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data and len(data) > 0:
            return data[0].get('lat'), data[0].get('lon')
    except requests.RequestException:
        return None, None
    return None, None

# ------------------ Views (Your existing ones, then the updated predict ones) ------------------

@api_view(['GET'])
def get_current_weather(request):
    geo = get_geolocation()
    API_KEY = os.getenv('OPENWEATHER_API_KEY')
    if geo and geo["latitude"] and geo["longitude"]:
        weather = get_weather(geo["latitude"], geo["longitude"], API_KEY)
    else:
        weather = None

    return Response({
        "city": geo.get("city") if geo else None,
        "temp": weather["temp"] if weather else None,
        "humidity": weather["humidity"] if weather else None,
        "description": weather["description"] if weather else None,
        "wind_speed": weather["wind_speed"] if weather else None,
    })

@api_view(['GET'])
def get_aqi(request):
    API_KEY = os.getenv('WEATHER_API_KEY') # Assuming this is your WeatherAPI.com key
    geo = get_geolocation()
    if not geo or not geo.get("latitude") or not geo.get("longitude"):
        return Response({"error": "Could not determine geolocation"}, status=status.HTTP_400_BAD_REQUEST)
    
    LATITUDE = geo["latitude"]
    LONGITUDE = geo["longitude"]
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={LATITUDE},{LONGITUDE}&aqi=yes"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pm25 = data.get("current", {}).get("air_quality", {}).get("pm2_5")
        if pm25 is None:
            return Response({"error": "PM2.5 data not available"}, status=500)
        real_aqi = compute_pm25_aqi(pm25)
        return Response({"AQI_Value": real_aqi})
    except requests.RequestException as e:
        return Response({"error": "Error fetching AQI data", "details": str(e)}, status=500)

@api_view(['GET'])
def get_weather_history(request):
    API_KEY = os.getenv('WEATHER_API_KEY')
    geo = get_geolocation()
    if not geo or not geo.get("latitude") or not geo.get("longitude"):
        return Response({"error": "Could not determine geolocation"}, status=status.HTTP_400_BAD_REQUEST)
    
    LATITUDE = geo["latitude"]
    LONGITUDE = geo["longitude"]
    history = []

    for i in range(1, 6):
        date = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        url = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={LATITUDE},{LONGITUDE}&dt={date}&aqi=yes"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            hist_data = resp.json()
            day_data = hist_data.get('forecast', {}).get('forecastday', [{}])[0]
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
def get_weather_forecast(request):
    API_KEY = os.getenv('OPENWEATHER_API_KEY')
    geo = get_geolocation()
    if not geo or not geo.get("latitude") or not geo.get("longitude"):
        return Response({"error": "Could not determine geolocation"}, status=status.HTTP_400_BAD_REQUEST)

    LATITUDE = geo["latitude"]
    LONGITUDE = geo["longitude"]
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}&units=metric"

    forecast_data = []
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        forecast_json = resp.json()
        daily = {}

        for entry in forecast_json.get('list', []):
            date = entry['dt_txt'].split(' ')[0]
            temp = entry['main']['temp']
            if date not in daily:
                daily[date] = {"temps": []}
            daily[date]["temps"].append(temp)

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
        forecast_data.append({"error": str(e)})

    return Response({"forecast": forecast_data})

@api_view(['GET'])
def get_alert(request):
    API_KEY = os.getenv('WEATHER_API_KEY')
    geo = get_geolocation()
    if not geo or not geo.get("latitude") or not geo.get("longitude"):
        return Response({"error": "Could not determine geolocation"}, status=status.HTTP_400_BAD_REQUEST)
    
    LATITUDE = geo["latitude"]
    LONGITUDE = geo["longitude"]
    url = f"http://api.weatherapi.com/v1/alerts.json?key={API_KEY}&q={LATITUDE},{LONGITUDE}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        alerts = response.json().get('alerts', {}).get('alert', [])
        if not alerts:
            return Response({"message": "No weather alerts at this time."})
        return Response({"alerts": alerts})
    except requests.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --- UPDATED PREDICT VIEWS ---

@api_view(['POST'])
def predict_geo(request):
    geo = get_geolocation()
    if not geo or not geo.get("city") or not geo.get("latitude") or not geo.get("longitude"):
        return Response({"error": "City or geolocation not found"}, status=400)

    city = geo["city"]
    latitude = geo["latitude"]
    longitude = geo["longitude"]

    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    current_weather_data = get_weather(latitude, longitude, OPENWEATHER_API_KEY)
    if not current_weather_data:
        return Response({"error": "Failed to fetch current weather data for prediction"}, status=500)

    model_path = settings.BASE_DIR.parent / 'ml' / 'models' / 'weather_model.pkl'
    encoder_path = settings.BASE_DIR.parent / 'ml' / 'models' / 'label_encoder.pkl'

    try:
        model = joblib.load(model_path)
        label_encoder = joblib.load(encoder_path)

        # Encode the city/district
        try:
            encoded_district = label_encoder.transform([city])[0] # Assuming 'city' maps to 'District' in your encoder
        except ValueError:
            return Response(
                {"error": f"City/District '{city}' not recognized by the model's encoder. Please select a different city or try another method."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract features from current_weather_data and define placeholders for others
        # Fill these based on the `MODEL_FEATURES` list and available data.
        # Use 0.0 or a reasonable default for features not directly available.
        # ORDER IS CRUCIAL!

        # Define placeholder for MinWindSpeed_10m as it's not readily available
        min_wind_speed_10m = 0.0 # Placeholder, ideally from training data mean/min

        # Define placeholders for 50m wind speeds
        wind_speed_50m = 0.0 # Placeholder
        max_wind_speed_50m = 0.0 # Placeholder
        min_wind_speed_50m_50m = 0.0 # Placeholder
        wind_speed_range_50m = 0.0 # Placeholder

        # Define placeholders for specialized temps
        wet_bulb_temp_2m = current_weather_data.get('temp') # As a proxy, or 0.0
        earth_skin_temp = current_weather_data.get('temp') # As a proxy, or 0.0

        # Calculate ranges
        temp_range_2m = current_weather_data.get('temp_max', 0.0) - current_weather_data.get('temp_min', 0.0)
        # Assuming MaxWindSpeed_10m is current_weather_data.get('wind_gust')
        wind_speed_range_10m = current_weather_data.get('wind_gust', 0.0) - min_wind_speed_10m


        input_data_list = [
            float(latitude), # Latitude
            float(longitude), # Longitude
            current_weather_data.get('precip', 0.0), # Precip
            current_weather_data.get('pressure', 1013.25), # Pressure (default to std atmospheric pressure)
            current_weather_data.get('humidity', 0.0), # Humidity_2m
            current_weather_data.get('humidity', 0.0), # RH_2m (assuming same as Humidity_2m)
            current_weather_data.get('temp', 0.0), # Temp_2m
            wet_bulb_temp_2m, # WetBulbTemp_2m (placeholder/proxy)
            current_weather_data.get('temp_max', 0.0), # MaxTemp_2m
            current_weather_data.get('temp_min', 0.0), # MinTemp_2m
            temp_range_2m, # TempRange_2m
            earth_skin_temp, # EarthSkinTemp (placeholder/proxy)
            current_weather_data.get('wind_speed', 0.0), # WindSpeed_10m
            current_weather_data.get('wind_gust', current_weather_data.get('wind_speed', 0.0)), # MaxWindSpeed_10m (using gust or speed)
            min_wind_speed_10m, # MinWindSpeed_10m (placeholder)
            wind_speed_range_10m, # WindSpeedRange_10m
            wind_speed_50m, # WindSpeed_50m (placeholder)
            max_wind_speed_50m, # MaxWindSpeed_50m (placeholder)
            min_wind_speed_50m_50m, # MinWindSpeed_50m (placeholder)
            wind_speed_range_50m, # WindSpeedRange_50m (placeholder)
            encoded_district # District_encoded
        ]

        # Verify the number of features before passing to the model
        if len(input_data_list) != 21:
            return Response({"error": f"Feature count mismatch: Expected 21, got {len(input_data_list)}. Please recheck `MODEL_FEATURES` and `input_data_list` construction."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # The model expects a 2D array: [[feature1, feature2, ..., feature21]]
        prediction = model.predict([input_data_list])

        print(f"Prediction result for {city}: {prediction[0]}")
        # Model predicts only one value, so return prediction[0]
        return Response({"predicted_temp": prediction[0]}, status=200)

    except Exception as e:
        print(f"Prediction error in predict_geo: {e}")
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
def predict_city(request):
    city = request.data.get('city')
    if not city:
        return Response({"error": "City name is required"}, status=400)

    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    
    # Step 1: Geocode city name to lat/lon
    latitude, longitude = get_lat_lon_from_city(city, OPENWEATHER_API_KEY)
    if not latitude or not longitude:
        return Response({"error": f"Could not determine geolocation for city: '{city}'"}, status=status.HTTP_400_BAD_REQUEST)

    # Step 2: Get current weather data for the geocoded lat/lon
    current_weather_data = get_weather(latitude, longitude, OPENWEATHER_API_KEY)
    if not current_weather_data:
        return Response({"error": "Failed to fetch current weather data for prediction for the specified city."}, status=500)

    model_path = settings.BASE_DIR.parent / 'ml' / 'models' / 'weather_model.pkl'
    encoder_path = settings.BASE_DIR.parent / 'ml' / 'models' / 'label_encoder.pkl'

    try:
        model = joblib.load(model_path)
        label_encoder = joblib.load(encoder_path)
        
        # Encode the city/district
        try:
            encoded_district = label_encoder.transform([city])[0]
        except ValueError:
            return Response(
                {"error": f"City/District '{city}' not recognized by the model's encoder. Please ensure it's a valid city for prediction."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract features and define placeholders - same logic as predict_geo
        min_wind_speed_10m = 0.0 # Placeholder
        wind_speed_50m = 0.0 # Placeholder
        max_wind_speed_50m = 0.0 # Placeholder
        min_wind_speed_50m_50m = 0.0 # Placeholder
        wind_speed_range_50m = 0.0 # Placeholder
        wet_bulb_temp_2m = current_weather_data.get('temp') # As a proxy, or 0.0
        earth_skin_temp = current_weather_data.get('temp') # As a proxy, or 0.0
        temp_range_2m = current_weather_data.get('temp_max', 0.0) - current_weather_data.get('temp_min', 0.0)
        wind_speed_range_10m = current_weather_data.get('wind_gust', 0.0) - min_wind_speed_10m

        input_data_list = [
            float(latitude), # Latitude
            float(longitude), # Longitude
            current_weather_data.get('precip', 0.0), # Precip
            current_weather_data.get('pressure', 1013.25), # Pressure
            current_weather_data.get('humidity', 0.0), # Humidity_2m
            current_weather_data.get('humidity', 0.0), # RH_2m
            current_weather_data.get('temp', 0.0), # Temp_2m
            wet_bulb_temp_2m, # WetBulbTemp_2m
            current_weather_data.get('temp_max', 0.0), # MaxTemp_2m
            current_weather_data.get('temp_min', 0.0), # MinTemp_2m
            temp_range_2m, # TempRange_2m
            earth_skin_temp, # EarthSkinTemp
            current_weather_data.get('wind_speed', 0.0), # WindSpeed_10m
            current_weather_data.get('wind_gust', current_weather_data.get('wind_speed', 0.0)), # MaxWindSpeed_10m
            min_wind_speed_10m, # MinWindSpeed_10m
            wind_speed_range_10m, # WindSpeedRange_10m
            wind_speed_50m, # WindSpeed_50m
            max_wind_speed_50m, # MaxWindSpeed_50m
            min_wind_speed_50m_50m, # MinWindSpeed_50m
            wind_speed_range_50m, # WindSpeedRange_50m
            encoded_district # District_encoded
        ]

        if len(input_data_list) != 21:
            return Response({"error": f"Feature count mismatch: Expected 21, got {len(input_data_list)}. Please recheck `MODEL_FEATURES` and `input_data_list` construction."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        prediction = model.predict([input_data_list])

        print(f"Prediction result for {city}: {prediction[0]}")
        return Response({"predicted_temp": prediction[0]}, status=200)

    except Exception as e:
        print(f"Prediction error in predict_city: {e}")
        return Response({"error": str(e)}, status=500)


# Your existing get_current_weather_default function (ensure it's below predict_city)
@api_view(['POST'])
def get_current_weather_default(request):
    city = request.data.get('city')
    if not city:
        return Response({'error': 'City field is required in the request body.'}, status=400)

    api_key = os.getenv('OPENWEATHER_API_KEY')
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