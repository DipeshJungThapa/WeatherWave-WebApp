# backend/favourite/serializers.py
from rest_framework import serializers
from .models import Favourite

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ['id', 'user', 'district_name', 'added_at'] # Assuming your model uses district_name
        read_only_fields = ['user', 'added_at']