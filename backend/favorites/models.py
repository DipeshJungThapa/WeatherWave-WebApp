# backend/favorites/models.py
from django.db import models
from django.conf import settings # Import settings to get AUTH_USER_MODEL

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    city_name = models.CharField(max_length=255)
    # You can add more fields if you want to store specific weather data for the favorite
    # e.g., temperature, weather_description, etc.

    class Meta:
        # Ensures a user can only favorite a city once
        unique_together = ('user', 'city_name',)
        ordering = ['city_name'] # Order favorites alphabetically by city name

    def __str__(self):
        return f"{self.city_name} (User: {self.user.username})"