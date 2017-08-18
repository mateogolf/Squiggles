"""TRAVELS URL"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^destination/(?P<trip_id>\d+)$', views.show),
    url(r'^(?P<trip_id>\d+)$', views.addSchedule),
    url(r'^create$', views.create),
    url(r'^add$', views.new),
    url(r'^$', views.index),
]
