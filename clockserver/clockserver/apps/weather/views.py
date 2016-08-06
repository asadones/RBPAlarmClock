import json
import requests

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


WEATHER_ICON_MAP = {
    'clear sky': 'wi-day-sunny',
    'few clouds': 'wi-day-cloudy',
    'scattered clouds': 'wi-day-cloudy',
    'broken clouds': 'wi-day-cloudy',
    'shower rain': 'wi-day-showers',
    'rain': 'wi-day-rain',
    'thunderstorm': 'wi-day-thunderstorm',
    'snow': 'wi-day-snow',
    'mist': 'wi-day-fog',
}


def _get_icon(description):
    return WEATHER_ICON_MAP.get(description)


def handle_weather(data):
    return {
        'temperature': int(data['main']['temp']),
        'label': data['weather'][0]['main'],
        'icon': _get_icon(data['weather'][0]['description']),
        'timestamp': data['dt'],
    }


class CurrentWeatherView(APIView):
    def get(self, request):
        parameters = {
            'id': settings.OPEN_WEATHER_MAP_LOCATION_ID,
            'appid': settings.OPEN_WEATHER_MAP_API_KEY,
            'units': request.GET.get('unit', 'metric'),
        }
        response = requests.get(
            settings.OPEN_WEATHER_MAP_API_ENDPOINT + 'weather',
            params=parameters)
        if response.status_code != status.HTTP_200_OK:
            return Response({
                'status': 'error',
                'code': response.status_code,
            })
        data = json.loads(response.content)
        return Response({
            'status': 'success',
            'weather': handle_weather(data),
            'location': ', '.join([
                data['name'],
                data['sys']['country'],
            ]),
        })


class WeatherForecastView(APIView):
    def get(self, request):
        parameters = {
            'id': settings.OPEN_WEATHER_MAP_LOCATION_ID,
            'appid': settings.OPEN_WEATHER_MAP_API_KEY,
            'units': request.GET.get('unit', 'metric'),
        }
        response = requests.get(
            settings.OPEN_WEATHER_MAP_API_ENDPOINT + 'forecast',
            params=parameters)
        if response.status_code != status.HTTP_200_OK:
            return Response({
                'status': 'error',
                'code': response.status_code,
            })
        data = json.loads(response.content)
        return Response({
            'status': 'success',
            'forecast': [handle_weather(weather) for weather in data['list']],
            'location': ', '.join([
                data['city']['name'],
                data['city']['country'],
            ]),
        })
