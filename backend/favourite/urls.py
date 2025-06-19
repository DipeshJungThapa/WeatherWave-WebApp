from django.urls import path
from . import views

app_name = 'favourite'

urlpatterns = [
    path('add/', views.add_favourite, name='add_favourite'),
    path('remove/<int:favourite_id>/', views.remove_favourite, name='remove_favourite'),
    path('list/', views.list_favourites, name='list_favourites'),
]
