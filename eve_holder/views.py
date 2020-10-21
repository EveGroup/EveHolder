"""This module contains views of the website."""
from django.shortcuts import render

from .models import Event

def homepage(request):
    event_list = Event.objects.all()
    context = {'events': event_list}

    return render(request, 'eve_holder/homepage.html', context)


def event_detail(request):
    return render(request, 'eve_holder/event_detail.html')
