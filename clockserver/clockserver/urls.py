"""clockserver URL Configuration"""
from django.conf.urls import url
from django.contrib import admin

from clockserver.views import HomeView


urlpatterns = [
    url(r'^$', HomeView.as_view()),
]
