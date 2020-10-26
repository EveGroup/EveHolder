from django_filters import FilterSet

from .models import *


class EventFilter(FilterSet):
    class Meta:
        model = Event
        fields = ['event_name', 'event_description']
        exclude = ['event_description', 'date_created', 'host', 'visitor']
