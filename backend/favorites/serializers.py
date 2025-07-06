# backend/favorites/serializers.py
from rest_framework import serializers
from .models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'city_name'] # 'id' is good for frontend reference
        read_only_fields = ['user'] # User is set automatically by the view