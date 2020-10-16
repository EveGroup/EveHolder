"""This module is control about url pattern for using in website."""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
