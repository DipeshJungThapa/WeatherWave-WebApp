"""
URL configuration for weatherwave_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:   from my_app import views
    2. Add a URL to urlpatterns:   path('', views.home, name='home')
Class-based views
    1. Add an import:   from other_app.views import Home
    2. Add a URL to urlpatterns:   path('', Home.as_view(), name='home')
Including another URLconf
    1.  Import the include() function: from django.urls import include, path
    2.  Add a URL to urlpatterns:   path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path,include
from django.http import JsonResponse
from forecast.views import * # This will import all views from forecast, including predict_city/geo
from rest_framework.routers import DefaultRouter
from knox import views as knox_views
from Login_Auth.views import RegisterViewset, LoginViewset,UserViewset

# weatherwave_project/urls.py

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include # <--- Make sure 'include' is here
from django.http import JsonResponse
from forecast.views import * # <--- KEEP THIS LINE! We need these views directly here.
from rest_framework.routers import DefaultRouter
from knox import views as knox_views
from Login_Auth.views import RegisterViewset, LoginViewset,UserViewset

router= DefaultRouter()
router.register("register", RegisterViewset, basename="register")
router.register("login", LoginViewset, basename="login")
router.register("users", UserViewset, basename="users")

def home(request):
    return JsonResponse({"message": "Welcome to WeatherWave API!"})

# All URLs are combined into one list, then the 'router.urls' are prepended
urlpatterns = router.urls + [
    path("admin/", admin.site.urls),
    path("logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("logout-all/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),

    # *** THIS IS THE KEY CHANGE FOR ALL YOUR API ENDPOINTS ***
    # This single line will group all your API-related paths under '/api/'
    path('api/', include([
        # Forecast app URLs (directly using the imported views)
        path('current-weather/', get_current_weather, name='api-current-weather'),
        path('default-weather/', get_current_weather_default, name='api-default-weather'),
        path('aqi/', get_aqi, name='api-aqi'),
        path('history/', get_weather_history, name='api-history'),
        path('forecast/', get_weather_forecast, name='api-forecast'),
        path('alert/', get_alert, name='api-alert'),
        path('weather-news/', get_weather_news, name='api-weather-news'),
        path('predict-city/', predict_city, name='api-predict-city'),
        path('predict-geo/', predict_geo, name='api-predict-geo'),

        # Favorites app URLs (included from its own urls.py)
        # Note the empty string path; this means favorites.urls' paths
        # (like 'favorites/') will directly follow 'api/'
        path('', include('favorites.urls')),

    ])), # <--- IMPORTANT: Closing bracket and parenthesis for the include([ ... ])

    path('', home), # Your root welcome message
]