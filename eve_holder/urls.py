from django.urls import path

from . import views

app_name = 'eve_holder'
urlpatterns = [
    # authenticate part
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('register/', views.register_page, name="register"),

    # unautherticated user
    path('', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # visitor part
    path('visitor/', views.visitors, name="visitors"),
    path('informations/<str:pk>/', views.visitor_information, name="information"),
    path('events/', views.events, name="events"),
    path('events/<int:pk>/register', views.event_register, name='event_register'),

    # host part
    path('host/', views.host, name="host"),
    path('events/<int:pk>/visitors', views.visitors_list, name="visitors_list"),  # List visitor in the event
    path('create_event/', views.create_event, name="create_event"),
    path('edit_event/<str:pk>/', views.edit_event, name="edit_event"),
    path('delete_event/<str:pk>/', views.delete_event, name="delete_event"),

    # both host and visitor use
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
]
