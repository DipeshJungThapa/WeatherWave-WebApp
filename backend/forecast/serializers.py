from rest_framework import serializers
from .models import Weather
class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ['id', 'city', 'temperature', 'description', 'date']
        read_only_fields = ['id']
    
    def validate_temperature(self, value):
        if value < -100 or value > 100:
            raise serializers.ValidationError("Temperature must be between -100 and 100 degrees.")
        return value