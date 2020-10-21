"""This module contain models to set layout for database.
TODO: implement the models class is this can be better with separate file.
"""

from django.db import models
from django.utils import timezone


class Host(models.Model):
    """Create host table in database.
    Collect name, email, phone_num of Host into database.
    Notes:
        host_name: host's name.
        host_email: host's email.
        host_phone_num: host's phone number.
    """
    host_name = models.CharField(max_length=100, null=True)
    host_email = models.EmailField(max_length=200, null=True)
    host_phone_num = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.host_name


class Event(models.Model):
    """Create event table in database.
    Collect event_name, description, host
    pub_date, and end_date detail into database
    Notes:
        event_name: name of that event.
        event_description: explain about event.
        event_host: defined who create that event.
        pub_date: date that let the visitors registration into the event.
        end_date: ending date of the event.
    """
    event_name = models.CharField(max_length=500, null=True)
    event_description = models.CharField(max_length=500, null=True, blank=True)
    event_host = models.ManyToManyField(Host)
    pub_date = models.DateTimeField('published date', null=True)
    end_date = models.DateTimeField('ending date', null=True)

    def can_register(self):
        """Check the event that can registration or not.
        Returns:
             bool: true if now was between pub_date and end_date.
        """
        now = timezone.now()
        return self.pub_date <= now <= self.end_date

    def is_expired(self):
        """Check the expiration date or end date of the event.
        Returns:
             bool: true if now was more than end_date.
        """
        now = timezone.now()
        return now > self.end_date

    def __str__(self):
        """Display the event's name."""
        return self.event_name

    can_register.boolean = True


class Visitor(models.Model):
    """Create visitors' table in database.
    Collect name, phone_num, email,
    event_already_regis, and event_history into database.
    Notes:
        visitor_name: visitor's name.
        visitor_phone_num: visitor's phone number.
        visitor_email: visitor's email.
        visitor_event_already_regis: visitor's registration event.
        visitor_event_history: history of event from each visitor.
    """
    visitor_name = models.CharField(max_length=150, null=True)
    visitor_phone_num = models.CharField(max_length=100, null=True)
    visitor_email = models.EmailField(max_length=100, null=True)
    visitor_event = models.ManyToManyField(Event, blank=True)

    def __str__(self):
        return self.visitor_name
