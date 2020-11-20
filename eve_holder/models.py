"""This module contain models to set layout for database."""
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


def get_now_with_delta_one():
    return timezone.now() + timedelta(days=1)


def get_now_with_delta_two():
    return timezone.now() + timedelta(days=2)


class Host(models.Model):
    """Create host table in database.

    Collect name, email, phone_num of Host into database.

    Notes:
        name: host's name.
        email: host's email.
        phone_num: host's phone number.
    """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True)
    email = models.EmailField(max_length=200, null=True)
    phone_num = models.CharField(max_length=100, null=True)

    def __str__(self):
        """Display host's name."""
        return self.name


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
    event_location = models.CharField(max_length=1000, null=True)
    pub_date = models.DateTimeField('published date', null=True, default=timezone.now)
    end_date = models.DateTimeField('ending date', null=True, default=get_now_with_delta_two)
    amount_accepted = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1)], default=5)
    event_date = models.DateField('event date', null=True, default=get_now_with_delta_one)

    def can_register(self):
        """Check if the event can be registered.

        Returns:
             bool: true if the event can be registered.
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

    def is_full(self, amount):
        return amount > self.amount_accepted

    def __str__(self):
        """Display the event's name."""
        return self.event_name

    can_register.boolean = True


class Visitor(models.Model):
    """Create visitors' table in database.

    Collect name, phone_num, email,
    event_already_regis, and event_history into database.

    Notes:
        name: visitor's name.
        phone_num: visitor's phone number.
        email: visitor's email.
        visitor_event_already_regis: visitor's registration event.
        visitor_event_history: history of event from each visitor.
    """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True)
    phone_num = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    event = models.ManyToManyField(Event, blank=True)

    private = models.BooleanField(default=False, null=True)

    def is_private(self):
        """Return True if this visitor data is private."""
        return self.private

    def __str__(self):
        """Display visitor's name."""
        return self.name


class Notification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=75, null=True)
    level = models.TextField(max_length=150, null=True)
    visitor = models.ManyToManyField(Visitor, through='NotificationUser')

    def __str__(self):
        """Return Notification's text"""
        return self.text


class NotificationUser(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, null=True)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, null=True)

    def __str__(self):
        """Return Notification's text"""
        return str(self.notification)