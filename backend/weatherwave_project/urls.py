# backend/weatherwave/urls.py
"""
URL configuration for weatherwave_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1.  Import the include() function: from django.urls import include, path
    2.  Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include # Removed login_required, JsonResponse
from forecast.views import * # Import all views from forecast
# Removed: from rest_framework.routers import DefaultRouter
# Removed: from knox import views as knox_views
# Removed: from Login_Auth.views import RegisterViewset, LoginViewset,UserViewset

# Removed: router = DefaultRouter() and router.register calls

def home(request):
    # This will still return a JSON message, but it's not a critical part of the dashboard
    return JsonResponse({"message": "Welcome to WeatherWave API! (Authentication removed for data access)"})


urlpatterns = [
    path("admin/", admin.site.urls),
    # Removed authentication related paths and router.urls
    # path("login/",knox_views.LoginView.as_view(), name="knox_logoutall"),
    # path("logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    
    # Data fetching endpoints (now publicly accessible)
    path('weather/', get_current_weather),
    path('default_weather/',get_current_weather_default),
    path('aqi/', get_aqi),
    path('predict_geo/', predict_geo),
    path('predict_city/', predict_city),
    path('history/', get_weather_history),
    path('forecast/', get_weather_forecast),
    path("alert/",get_alert),
    
    # Favourites are still included but will show a message on frontend
    # Removed: path('favourite/', login_required(include('favourite.urls'))),
    path('favourite/', include('favourite.urls')),
    
    # Removed: path("api/auth/", include('knox.urls')),
    path('', home), # The root path
]