
"""Module for tests event."""
import datetime

from django.test import TestCase
from eve_holder.models import Event
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse

class EventTest(TestCase):
    """Test register event and expired date."""
    def test_pass_event_register(self):
        """After end date cannot register."""
        time = timezone.now() + datetime.timedelta(days=-2)
        pass_event = Event(event_name="pass event", pub_date=time, end_date=time + datetime.timedelta(days=-1))
        self.assertIs(pass_event.can_register(), False)

    def test_can_register(self):
        """Before end date cannot register."""
        time = timezone.now()
        pass_event = Event(event_name="pass event", pub_date=time, end_date=time + datetime.timedelta(days=30))
        self.assertIs(pass_event.can_register(), True)

    def test_is_expire(self):
        """Expired date after end date."""
        time = timezone.now() + datetime.timedelta(days=-2)
        pass_event = Event(event_name="pass event", pub_date=time, end_date=time + datetime.timedelta(days=-1))
        self.assertIs(pass_event.is_expired(), True)
       

class TestAuth(TestCase):

    def setUp(self) -> None:
        user = User.objects.create_user('Test', 'test@gmail.com', 'testPassword')

    def test_visitors(self):
        url = reverse('eve_holder:visitors', )
