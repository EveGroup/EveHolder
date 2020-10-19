from django.db import models

# Create your models here.

class Visitor(models.Model):
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Host(models.Model):
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    STATUS = (
            ('Upcoming', 'Upcoming'),
            ('Ended', 'Ended'),
            )
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=100, null=True, choices=STATUS)
    location = models.CharField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    tag = models.ManyToManyField(Tag)
    host = models.ForeignKey(Host, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    
class Ticket(models.Model):
    STATUS = (
            ('Available', 'Available'),
            ('Reserved', 'Reserved'),
            ('Expired', 'Expired'),
            )
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    visitor = models.ForeignKey(Visitor, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=100, null=True, choices=STATUS)

    def __str__(self):
        return f"{self.event.name}'s Ticket for {self.visitor.name}'"
