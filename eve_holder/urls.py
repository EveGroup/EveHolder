"""This module is control about url pattern for using in website."""
from django.urls import path
from django.contrib import admin

from . import views

app_name = 'eve_holder'
urlpatterns = [
    path('', views.HomepageView.as_view(), name='blank_homepage'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    # path('admin/', admin.site.urls, name='admin'),  # click at log in as host = go to host login page
    path('home/', views.HomepageView.as_view(), name='homepage')
]
