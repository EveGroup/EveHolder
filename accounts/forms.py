from django.forms import ModelForm
from .models import *


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
 