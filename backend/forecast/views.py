from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Weather
from .serializers import WeatherSerializer
import requests
import datetime

def get_weatherapi_weather(lat, lon, api_key):
    # Get current weather
    current_url = (
        f"http://api.weatherapi.com/v1/current.json?"
        f"key={api_key}&q={lat},{lon}&aqi=yes"
    )
    result = {}

    try:
        response = requests.get(current_url)
        response.raise_for_status()
        data = response.json()
        location = data['location']
        current = data['current']
        result['current'] = {
            "location": location,
            "weather": current,
            "aqi": current.get('air_quality', {})
        }
    except requests.RequestException as e:
        result['current'] = {"error": str(e)}



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
    geo= get_geolocation()
    if not geo or not geo.get("latitude") or not geo.get("longitude"):
        return Response({"error": "Could not determine geolocation"}, status=status.HTTP_400_BAD_REQUEST)
    LATITUDE = geo["latitude"]
    LONGITUDE = geo["longitude"]

    # Get current AQI
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
        current_aqi = {
            "CO": aqi.get('co'),
            "NO2": aqi.get('no2'),
            "O3": aqi.get('o3'),
            "SO2": aqi.get('so2'),
            "PM2_5": aqi.get('pm2_5'),
            "PM10": aqi.get('pm10'),
            "US_EPA_Index": aqi.get('us-epa-index'),
            "GB_DEFRA_Index": aqi.get('gb-defra-index'),
        }
    except requests.RequestException as e:
        return Response({"error": "Error fetching AQI data", "details": str(e)}, status=500)
    
    return Response({
        "current_aqi": current_aqi,
     })
    

@api_view(['GET'])
def get_weather_history(request):
    API_KEY = "4b6340b064804275bff164431252305"
    geo= get_geolocation()
    if not geo or not geo.get("latitude") or not geo.get("longitude"):
        return Response({"error": "Could not determine geolocation"}, status=status.HTTP_400_BAD_REQUEST)
    LATITUDE = geo["latitude"]
    LONGITUDE = geo["longitude"]

    history = []
    for i in range(1, 6):
        date = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        history_url = (
            f"http://api.weatherapi.com/v1/history.json?"
            f"key={API_KEY}&q={LATITUDE},{LONGITUDE}&dt={date}&aqi=yes"
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

    return Response({"history": history,})

@api_view(['GET'])
def get_weather_forecast(request):
    # 5-day/3-hour forecast (returns data every 3 hours for 5 days)
    API_KEY = "80397f82704fe5be4137c087667e2e31"
    LATITUDE = "27.7017"  # Example: Kathmandu
    LONGITUDE = "85.320"  # Example: Kathmandu

    forecast_url = (
        f"http://api.openweathermap.org/data/2.5/forecast?"
        f"lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}&units=metric"
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
    API_KEY = "4b6340b064804275bff164431252305"
    geo= get_geolocation()
    if not geo or not geo.get("latitude") or not geo.get("longitude"):
        return Response({"error": "Could not determine geolocation"}, status=status.HTTP_400_BAD_REQUEST)
    LATITUDE = geo["latitude"]
    LONGITUDE = geo["longitude"]
    alert_url = (
        f"http://api.weatherapi.com/v1/alerts.json?"
        f"key={API_KEY}&q={LATITUDE},{LONGITUDE}"
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
def predict_temp(request):
    features = request.data  # Expect JSON with features like humidity, wind speed, etc.
    # Load model & predict here
    return Response({"predicted_temp": 28})
#added 5 din ko kura


from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

@api_view(['POST'])
def get_current_weather_default(request):
    # Get city name from POST data (text input)
    city = request.data.get('city')
    if not city:
        return Response({'error': 'City field is required in the request body.'}, status=400)
    
    api_key = '80397f82704fe5be4137c087667e2e31'
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