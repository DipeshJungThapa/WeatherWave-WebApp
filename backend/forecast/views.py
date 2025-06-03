from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_current_weather(request):
    city = request.GET.get('city')
    # Call weather API here
    return Response({"city": city, "temp": 27, "humidity": 60})

@api_view(['GET'])
def get_aqi(request):
    city = request.GET.get('city')
    # Call AQI API here
    return Response({"city": city, "PM2.5": 90, "PM10": 120})

'''@api_view(['POST'])
def predict_temp(request):
    features = request.data  # Expect JSON with features like humidity, wind speed, etc.
    # Load model & predict here
    return Response({"predicted_temp": 28})
'''