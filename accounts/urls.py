from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('register/', views.register_page, name="register"),
    
    path('', views.home, name="home"),
    path('events/', views.events, name="events"),
    path('visitors/<str:pk>/', views.visitors, name="visitors"),

    path('create_ticket/<str:pk>/', views.create_ticket, name="create_ticket"),
    path('update_ticket/<str:pk>/', views.update_ticket, name="update_ticket"),
    path('delete_ticket/<str:pk>/', views.delete_ticket, name="delete_ticket"),
]
