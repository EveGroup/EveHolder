""""""
import datetime

from django.db import models
from django.utils import timezone


class Host(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone_num = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']


class Event(models.Model):
    event_name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    host = models.ManyToManyField(Host)
    pub_date = models.DateTimeField('published date')
    end_date = models.DateTimeField('ending date')

    class Meta:
        ordering = ['event_name']

    def __str__(self):
        return self.event_name

    def can_register(self):
        """

        :rtype: true if now was between pub_date and end_date.
        """
        now = timezone.now()
        return self.pub_date <= now <= self.end_date

    def is_expired(self):
        """

        :rtype: true if now was more than end_date.
        """
        now = timezone.now()
        return now > self.end_date

    def is_visitor_register(self):
        pass

    def is_full(self):
        pass


class InformationVisitor(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, primary_key=True, )
    name = models.CharField(max_length=150)  # visitor name
    phone_num = models.CharField(max_length=100)
    optional = models.IntegerField()


class Visitors(models.Model):
    name = models.CharField(max_length=150)
    phone_num = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    event_already_regis = models.ForeignKey(InformationVisitor, on_delete=models.CASCADE)
    event_history = models.ForeignKey(Event, on_delete=models.CASCADE)

    def has_regis(self):
        pass

    def regis_event(self):
        pass
