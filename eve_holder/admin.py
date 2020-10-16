"""Display admin page for Host to create an event."""
from django.contrib import admin

from .models import Host, Event, InformationVisitor

admin.site.register(Host)
admin.site.register(Event)
admin.site.register(InformationVisitor)
