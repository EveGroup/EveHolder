from django.urls import path

from .views import visitor_signup_view
from django.views.generic.base import TemplateView

urlpatterns = [
    # path('', TemplateView.as_view(template_name='home.html'), name='home')
    # path('signup/', visitor_signup_view.as_view(), name='signup'),
    path('signup/', visitor_signup_view, name='signup')
]