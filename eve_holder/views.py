"""This module contains views of the website."""
from django.shortcuts import render

from .models import *


def home(request):
    return render(request, 'accounts/dashboard.html')


def events(request):
    event_list = Event.objects.all()
    return render(request, 'accounts/event.html', {'events': event_list})


def visitor(request):
    return render(request, 'accounts/visitor.html')
