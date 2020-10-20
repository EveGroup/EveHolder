from django.db import models

# Create your models here.

class Visitor(models.Model):
    visitor_name = models.CharField(max_length=100, null=True)
    visitor_phone = models.CharField(max_length=50, null=True, blank=True)
    visitor_email = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.visitor_name

class Host(models.Model):
    host_name = models.CharField(max_length=100, null=True)
    host_phone = models.CharField(max_length=50, null=True, blank=True)
    host_email = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.host_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.tag_name

class Event(models.Model):
    event_name = models.CharField(max_length=100, null=True)
    event_description = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    tag = models.ManyToManyField(Tag)
    host = models.ForeignKey(Host, null=True, on_delete=models.SET_NULL)
    visitor = models.ManyToManyField(Visitor)

    def __str__(self):
        return self.event_name
