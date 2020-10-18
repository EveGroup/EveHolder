from django.urls import path

from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('event/', views.event, name='event'),
    path('visitor/', views.visitor, name='Visitor')
]