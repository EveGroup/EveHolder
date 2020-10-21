"""This module is control about url pattern for using in website."""
from django.urls import path
from django.contrib import admin

from . import views

app_name = 'eve_holder'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
]
