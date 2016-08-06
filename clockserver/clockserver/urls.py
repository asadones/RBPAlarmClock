"""clockserver URL Configuration"""
from django.conf.urls import url, include

from clockserver.views import HomeView


urlpatterns = [
    url(r'^$', HomeView.as_view()),
    url(r'^weather/', include('clockserver.apps.weather.urls')),
]
