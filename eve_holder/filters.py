"""This module contains the filter for events."""
from django_filters import FilterSet

from .models import Event


class EventFilter(FilterSet):
    """This will filter the things we need in event."""
    class Meta:
        """TODO: What is meta?"""
        model = Event
        fields = ['event_name', 'event_description']
        exclude = ['event_description', 'date_created', 'host', 'visitor']
