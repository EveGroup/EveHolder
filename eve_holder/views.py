"""This module contains views of the website."""
from django.shortcuts import render

from .models import *


def home(request):
    visitor_list = Visitor.objects.all()
    event_list = Event.objects.all()

    total_events = event_list.count()

    context = {'events': event_list, 'visitors': visitor_list, 'total_events': total_events}

    return render(request, 'eve_holder/dashboard.html', context)


def events(request):
    event_list = Event.objects.all()
    return render(request, 'eve_holder/event.html', {'events': event_list})


def visitor(request, pk):
    visitors_list = Visitor.objects.get(id=pk)

    event_list = visitors_list.visitor_event.all()
    event_count = event_list.count()

    context = {'visitors': visitors_list, 'events': event_list, 'event_count': event_count}
    return render(request, 'eve_holder/visitor.html', context)
