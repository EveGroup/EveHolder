from django.urls import path
from django.contrib import admin

from . import views

app_name = 'eve_holder'
urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('register/', views.register_page, name="register"),
    
    path('', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('events/', views.events, name="events"),
    path('visitors/<str:pk>/', views.visitors, name="visitors"),

    path('create_event/<str:pk>/', views.create_event, name="create_event"),
    path('edit_event/<str:pk>/', views.edit_event, name="edit_event"),
    path('delete_event/<str:pk>/', views.delete_event, name="delete_event"),
]
