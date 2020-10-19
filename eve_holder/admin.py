"""Display admin page for Host to create an events."""
from django.contrib import admin

from .models import Host, Event

admin.site.register(Host)
admin.site.register(Event)
