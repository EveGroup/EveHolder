"""This module is control about url pattern for using in website."""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('event/', views.signup, name='event'),
    path('visitor/', views.login, name='visitor'),
]
