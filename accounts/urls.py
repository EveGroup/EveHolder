from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('events/', views.events, name="events"),
    path('visitors/<str:pk_test>/', views.visitors, name="visitors"),

    path('create_ticket/', views.createTicket, name="create_ticket"),
    path('update_ticket/<str:pk>/', views.updateTicket, name="update_ticket"),
    path('delete_ticket/<str:pk>/', views.deleteTicket, name="delete_ticket"),
]
