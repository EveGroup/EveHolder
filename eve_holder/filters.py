from django_filters import FilterSet

from .models import *


class EventFilter(FilterSet):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['event_description', 'date_created', 'host', 'visitor', 'tag']
