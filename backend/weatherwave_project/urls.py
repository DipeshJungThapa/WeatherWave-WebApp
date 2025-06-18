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
from django.urls import path,include
from django.http import JsonResponse
from forecast.views import * 
from rest_framework.routers import DefaultRouter
from knox import views as knox_views
from Login_Auth.views import RegisterViewset, LoginViewset,UserViewset

router= DefaultRouter()
router.register("register", RegisterViewset, basename="register")
router.register("login", LoginViewset, basename="login")
router.register("users", UserViewset, basename="users")

def home(request):
    return JsonResponse({"message": "Welcome to WeatherWave API!"})

urlpatterns = router.urls + [
    path("admin/", admin.site.urls),
    path("logoutall/",knox_views.LoginView.as_view(), name="knox_logoutall"),
    path("logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path('weather/', get_current_weather),
    path('aqi/', get_aqi),
    path('predict/', predict_temp),
    path('history/', get_weather_history),
    path('forecast/', get_weather_forecast),
    path("alert/",get_alert),
    #path("api/auth/", include('knox.urls')), 
    path('', home),
]

yeslai ahile delete garne
