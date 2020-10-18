"""This module contains views of the website."""
from django.http import HttpResponse
from django.views import generic

from .models import Event


class HomepageView(generic.ListView):
    template_name = 'eve_holder/homepage.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        return Event.objects.all()


class EventDetailView(generic.ListView):
    template_name = 'eve_holder/event_detail.html'

    def get_queryset(self):
        return HttpResponse("from event detail")
