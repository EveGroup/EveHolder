from django.urls import path

from . import views

app_name = 'eve_holder'

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('visitor/<str:pk>/', views.visitor, name='visitor'),

    path('create_event/', views.create_event, name='create_event'),
    path('edit_event/<str:pk>/', views.edit_event, name='edit_event'),
    path('delete_event/<str:pk>/', views.delete_event, name='delete_event')

]
