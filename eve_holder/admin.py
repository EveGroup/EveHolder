from django.contrib import admin

# Register your models here.
from .models import Host, Visitor, Event


admin.site.register(Event)
admin.site.register(Host)
admin.site.register(Visitor)
