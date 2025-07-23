# backend/favorites/admin.py
from django.contrib import admin
from .models import Favorite

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'city_name',)
    search_fields = ('user__username', 'city_name',) # Allows searching by username and city
    list_filter = ('user',) # Allows filtering by user