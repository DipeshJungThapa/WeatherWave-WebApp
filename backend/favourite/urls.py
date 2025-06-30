
# backend/favourite/urls.py
from django.urls import path
from . import views

app_name = 'favourite'

urlpatterns = [
    path('add/', views.add_favourite, name='add_favourite'),
    path('remove/', views.remove_favourite, name='remove_favourite'), # CHANGED: Removed <int:favourite_id>/
    path('list/', views.list_favourites, name='list_favourites'),
]