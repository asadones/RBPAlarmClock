"""clockserver URL Configuration"""
from django.conf.urls import url

from clockserver.apps.weather.views import CurrentWeatherView, WeatherForecastView


urlpatterns = [
    url(r'^current$', CurrentWeatherView.as_view()),
    url(r'^forecast$', WeatherForecastView.as_view()),
]
