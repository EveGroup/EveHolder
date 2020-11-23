from django.urls import path

from . import views

app_name = 'eve_holder'
urlpatterns = [
    # authenticate part
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('register/', views.register_page, name="register"),

    # unauthenticated user
    path('', views.homepage, name='homepage'),

    # visitor part
    path('visitor_registered_events/', views.visitor_registered_events, name="visitor_registered_events"),
    path('events/', views.events, name="events"),
    path('events/update_information', views.visitor_update_information, name='visitor_update_information'),
    # path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk_event>/register', views.event_register, name='event_register'),
    path('events/<int:pk_event>/cancel', views.cancel_event, name='event_cancel'),
    path('close-notification/<int:pk>/', views.close_notification, name='close_notification'),

    # host part
    path('host/', views.host, name="host"),
    path('host/update_information', views.host_update_information, name='host_update_information'),
    # host event
    path('create_event/', views.create_event, name="create_event"),
    path('edit_event/<str:pk>/', views.edit_event, name="edit_event"),
    path('delete_event/<str:pk>/', views.delete_event, name="delete_event"),
    # visitor_registered_events in event
    path('visitors_list/<str:pk>/', views.visitors_list, name="visitors_list"),
    path('informations/<str:pk>/', views.visitor_information, name="information"),

    # both host and visitor use
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('account/', views.my_account, name='my_account'),
    path('search/', views.search_event, name='search_event'),
]
