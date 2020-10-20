from django_filters import FilterSet, DateFilter

from .models import *

class TicketFilter(FilterSet):
    class Meta:
        model = Ticket
        fields = '__all__'
        exclude = ['visitor', 'date_created']
