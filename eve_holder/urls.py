from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('register/', views.register_page, name="register"),
    
    path('', views.home, name="home"),
    path('events/', views.events, name="events"),
    path('visitors/<str:pk>/', views.visitors, name="visitors"),

    path('create_event/<str:pk>/', views.create_event, name="create_event"),
    path('edit_event/<str:pk>/', views.edit_event, name="edit_event"),
    path('delete_event/<str:pk>/', views.delete_event, name="delete_event"),
]
