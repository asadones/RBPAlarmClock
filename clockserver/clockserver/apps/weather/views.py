import calendar
import json
import pytz
import requests

from datetime import datetime
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


WEATHER_ICON_DAY_MAP = {
    'clear sky': 'wi-day-sunny',
    'few clouds': 'wi-day-cloudy',
    'scattered clouds': 'wi-day-cloudy',
    'broken clouds': 'wi-day-cloudy',
    'shower rain': 'wi-day-showers',
    'light rain': 'wi-day-hail',
    'rain': 'wi-day-rain',
    'thunderstorm': 'wi-day-thunderstorm',
    'snow': 'wi-day-snow',
    'mist': 'wi-day-fog',
}

WEATHER_ICON_NIGHT_MAP = {
    'clear sky': 'wi-night-clear',
    'few clouds': 'wi-night-alt-partly-cloudy',
    'scattered clouds': 'wi-night-alt-cloudy',
    'broken clouds': 'wi-night-alt-cloudy',
    'shower rain': 'wi-night-alt-showers',
    'light rain': 'wi-night-alt-hail',
    'rain': 'wi-night-alt-rain',
    'thunderstorm': 'wi-day-alt-lightning',
    'snow': 'wi-night-alt-snow',
    'mist': 'wi-night-fog',
}


def _get_icon(description, sunrise=None, sunset=None):
    now = datetime.now(pytz.UTC)
    if sunrise and sunset and is_nighttime(now, sunrise, sunset):
        return WEATHER_ICON_NIGHT_MAP.get(description)
    return WEATHER_ICON_DAY_MAP.get(description)


def is_nighttime(dtime, sunrise, sunset):
    utc_timestamp = calendar.timegm(dtime.utctimetuple())
    return utc_timestamp < sunrise or utc_timestamp > sunset


def handle_weather(data):
    return {
        'temperature': int(data['main']['temp']),
        'label': data['weather'][0]['description'],
        'icon': _get_icon(
            data['weather'][0]['description'],
            sunrise=data.get('sys', {}).get('sunrise'),
            sunset=data.get('sys', {}).get('sunset'),
        ),
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
            'forecast': [
                handle_weather(weather)
                for weather in sorted(data['list'], key=lambda x: x['dt'])],
            'location': ', '.join([
                data['city']['name'],
                data['city']['country'],
            ]),
        })
