from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

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
            "city": data.get('city'),
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
def get_current_weather(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')
    city = request.query_params.get('city')
    API_KEY = os.getenv('OPENWEATHER_API_KEY')

    if lat and lon:
        weather = get_weather(lat, lon, API_KEY)
        city_name = city if city else (weather.get("city_name") if weather else None)
    elif city:
        lat, lon = get_lat_lon_from_city(city)
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

    return Response({
        "city": city_name,
        "temp": weather["temp"] if weather else None,
        "humidity": weather["humidity"] if weather else None,
        "description": weather["description"] if weather else None,
        "wind_speed": weather["wind_speed"] if weather else None,
    })

@api_view(['GET'])
def get_aqi(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')
    city = request.query_params.get('city')
    API_KEY = os.getenv('WEATHER_API_KEY')

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
def get_weather_history(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')
    city = request.query_params.get('city')
    API_KEY = os.getenv('WEATHER_API_KEY')

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
def get_weather_forecast(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')
    city = request.query_params.get('city')
    API_KEY = os.getenv('OPENWEATHER_API_KEY')

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
        forecast_data.append({"error": str(e)})

    return Response({
        "forecast": forecast_data
    })

@api_view(['GET'])
def get_alert(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')
    city = request.query_params.get('city')
    API_KEY = os.getenv('WEATHER_API_KEY')

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

    alert_url = (
        f"http://api.weatherapi.com/v1/alerts.json?"
        f"key={API_KEY}&q={query_lat},{query_lon}"
    )
    try:
        response = requests.get(alert_url)
        response.raise_for_status()
        data = response.json()
        alerts = data.get('alerts', {}).get('alert', [])
        if not alerts:
            return Response({"message": "No weather alerts at this time."})
        return Response({"alerts": alerts})
    except requests.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def predict_geo(request):
    geo = get_geolocation()
    if not geo or not geo.get("city"):
        return Response({"error": "Could not determine city from geolocation"}, status=status.HTTP_400_BAD_REQUEST)
    city = geo["city"]
    # Load your model here (replace with your actual model path and logic)
    # from sklearn.externals import joblib
    # model = joblib.load('your_model_path')
    # input_data = [[city]]
    # try:
    #     prediction = model.predict(input_data)
    #     return Response({"predicted_temp": prediction[0]}, status=status.HTTP_200_OK)
    # except Exception as e:
    #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"message": "Model prediction logic not implemented."})

@api_view(['POST'])
def predict_city(request):
    city = request.data.get('city')
    if not city:
        return Response({"error": "City name is required in the request body."}, status=status.HTTP_400_BAD_REQUEST)
    # Load your model here (replace with your actual model path and logic)
    # from sklearn.externals import joblib
    # model = joblib.load('your_model_path')
    # input_data = [[city]]
    # try:
    #     prediction = model.predict(input_data)
    #     return Response({"predicted_temp": prediction[0], status=status.HTTP_200_OK)
    # except Exception as e:
    #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"message": "Model prediction logic not implemented."})

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