from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Weather
from .serializers import WeatherSerializer
import requests

def get_weatherapi_weather(lat, lon, api_key):
   
    url = (
        f"http://api.weatherapi.com/v1/current.json?"
        f"key={api_key}&q={lat},{lon}&aqi=yes"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        location = data['location']
        current = data['current']
        # Display AQI if available
        if 'air_quality' in current:
            aqi = current['air_quality']
            print("Air Quality Index (AQI):")
            print(f"  - CO: {aqi.get('co')}")
            print(f"  - NO2: {aqi.get('no2')}")
            print(f"  - O3: {aqi.get('o3')}")
            print(f"  - SO2: {aqi.get('so2')}")
            print(f"  - PM2.5: {aqi.get('pm2_5')}")
            print(f"  - PM10: {aqi.get('pm10')}")
            print(f"  - US EPA Index: {aqi.get('us-epa-index')}")
            print(f"  - GB DEFRA Index: {aqi.get('gb-defra-index')}")
        else:
            print("Air Quality data not available.")
    except requests.RequestException as e:
        print("Error fetching weather data from WeatherAPI:")
        print(e)



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
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "temp": data['main']['temp'],
            "description": data['weather'][0]['description'],
            "humidity": data['main']['humidity'],
            "wind_speed": data['wind']['speed'],
        }
    except requests.RequestException:
        return None

@api_view(['GET'])
def get_current_weather(request):
    geo = get_geolocation()
    API_KEY = "80397f82704fe5be4137c087667e2e31"
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
    API_KEY = "4b6340b064804275bff164431252305"
    LATITUDE = "27.7017"  # Example: Kathmandu
    LONGITUDE = "85.320"  # Example: Kathmandu

    # Modified get_weatherapi_weather to return AQI data only(weather ahile liyena yeta bata)
    url = (
        f"http://api.weatherapi.com/v1/current.json?"
        f"key={API_KEY}&q={LATITUDE},{LONGITUDE}&aqi=yes"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        current = data.get('current', {})
        aqi = current.get('air_quality', {})
        return Response({
            "CO": aqi.get('co'),
            "NO2": aqi.get('no2'),
            "O3": aqi.get('o3'),
            "SO2": aqi.get('so2'),
            "PM2_5": aqi.get('pm2_5'),
            "PM10": aqi.get('pm10'),
            "US_EPA_Index": aqi.get('us-epa-index'),
            "GB_DEFRA_Index": aqi.get('gb-defra-index'),
        })
    except requests.RequestException as e:
        return Response({"error": "Error fetching AQI data", "details": str(e)}, status=500)

@api_view(['POST'])
def predict_temp(request):
    features = request.data  # Expect JSON with features like humidity, wind speed, etc.
    # Load model & predict here
    return Response({"predicted_temp": 28})
