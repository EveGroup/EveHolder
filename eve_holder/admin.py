"""Display admin page for Host to create an event."""

from django.contrib import admin

from .models import Host, Event, Visitor, Notification, NotificationUser

admin.site.register(Event)
admin.site.register(Host)
admin.site.register(Visitor)
admin.site.register(Notification)
admin.site.register(NotificationUser)