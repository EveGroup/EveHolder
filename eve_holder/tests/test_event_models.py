"""This module contains the test cases for the Event models."""
import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from eve_holder.models import Event
from eve_holder.tests import test_auth


def create_event(name: str, duration):
    """Use to create event object to test the programs.

    Args:
        name: event's name
        duration: time duration of an event

    Returns:
        Event: Event that user need to create.
    """
    pub_date = datetime.datetime.now() + datetime.timedelta(days=duration)
    end_date = pub_date + datetime.timedelta(days=abs(duration))
    return Event.objects.create(event_name=name, pub_date=pub_date, end_date=end_date)


class EventModelTest(TestCase):
    """Class for testing the event model."""

    def setUp(self) -> None:
        """Use to set up the test cases for EventModelTest class."""
        self.host = User.objects.create_user("Host", "test@gmail.com", "testPassword")

    def test_can_register_before_pubdate(self):
        """can_register() returns False for event whose pub_date is in the future."""
        pub_date = timezone.now() + datetime.timedelta(days=1)
        end_date = pub_date + datetime.timedelta(days=1)
        future_event = Event(event_name="Future Event", pub_date=pub_date, end_date=end_date)
        self.assertFalse(future_event.can_register())

    def test_can_register_in_register_date(self):
        """can_register() returns True for event whose that date is in the registration date."""
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = pub_date + datetime.timedelta(days=2)
        register_event = Event(event_name="Register Event", pub_date=pub_date, end_date=end_date)
        self.assertTrue(register_event.can_register())

    def test_can_register_after_end_date(self):
        """can_register() returns False for event that already ended."""
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = pub_date + datetime.timedelta(hours=20)
        old_event = Event(event_name="Old Event", pub_date=pub_date, end_date=end_date)
        self.assertFalse(old_event.can_register())

    def test_is_expired_before_pubdate(self):
        """can_register() returns False for event whose pub_date is in the future."""
        pub_date = timezone.now() + datetime.timedelta(days=1)
        end_date = pub_date + datetime.timedelta(days=1)
        future_event = Event(event_name="Future Event", pub_date=pub_date, end_date=end_date)
        self.assertFalse(future_event.is_expired())

    def test_is_expired_in_register_date(self):
        """is_expired() returns False for event whose pub_date is in the registration date."""
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = pub_date + datetime.timedelta(days=2)
        register_event = Event(event_name="Register Event", pub_date=pub_date, end_date=end_date)
        self.assertFalse(register_event.is_expired())

    def test_is_expired_after_end_date(self):
        """is_expired() returns True for event that already ended."""
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = pub_date + datetime.timedelta(hours=20)
        old_event = Event(event_name="Old Event", pub_date=pub_date, end_date=end_date)
        self.assertTrue(old_event.is_expired())

    def test_event_name(self):
        """Check the name of an event displayed correctly."""
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = pub_date + datetime.timedelta(days=2)
        register_event = Event(event_name="Register Event", pub_date=pub_date, end_date=end_date)
        self.assertEqual(str(register_event), "Register Event")
