"""This module contain models to set layout for database.

TODO: implement the models class is this can be better with separate file.
"""

from django.db import models
from django.utils import timezone


class Host(models.Model):
    """Create host table in database.

    Collect name, email, phone_num of Host into database.

    Notes:
        name: host's name.
        email: host's email.
        phone_num: host's phone number.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone_num = models.CharField(max_length=100)

    class Meta:
        """TODO: Search info about Meta class."""
        ordering = ['name']


class Event(models.Model):
    """Create event table in database.

    Collect event_name, description, host
    pub_date, and end_date detail into database

    Notes:
        event_name: name of that event.
        description: explain about event.
        host: defined who create that event.
        pub_date: date that let the visitors registration into the event.
        end_date: ending date of the event.
    """
    event_name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    host = models.ManyToManyField(Host)
    pub_date = models.DateTimeField('published date')
    end_date = models.DateTimeField('ending date')

    class Meta:
        """TODO: Search info about Meta class."""
        ordering = ['event_name']

    def __str__(self):
        """Display the event's name."""
        return self.event_name

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

    def is_visitor_register(self):
        """TODO: Please fill this."""
        pass

    def is_full(self):
        """TODO: Please fill this."""
        pass


class InformationVisitor(models.Model):
    """Create table in database for information visitor.

    Collect event, name, phone_num,
    and optional into database.

    Notes:
        event: collect that event when user input the information.
        name: visitor's name.
        phone_num: visitor's phone number.
    """
    event = models.OneToOneField(Event, on_delete=models.CASCADE, primary_key=True, )
    name = models.CharField(max_length=150)  # visitor name
    phone_num = models.CharField(max_length=100)
    optional = models.IntegerField()


class Visitors(models.Model):
    """Create visitors' table in database.

    Collect name, phone_num, email,
    event_already_regis, and event_history into database.

    Notes:
        name: visitor's name.
        phone_num: visitor's phone number.
        email: visitor's email.
        event_already_regis: visitor's registration event.
        event_history: history of event from each visitor.
    """
    name = models.CharField(max_length=150)
    phone_num = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    event_already_regis = models.ForeignKey(InformationVisitor, on_delete=models.CASCADE)
    event_history = models.ForeignKey(Event, on_delete=models.CASCADE)

    def has_regis(self):
        """TODO: Please fill this."""
        pass

    def regis_event(self):
        """TODO: Please fill this."""
        pass
