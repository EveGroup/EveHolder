import datetime

from django.test import TestCase
from django.utils import timezone

from eve_holder.models import Event


def create_event(name: str, duration: datetime):
    pub_date = datetime.datetime.now() + datetime.timedelta(days=duration)
    end_date = pub_date + datetime.timedelta(days=abs(duration))
    return Event.objects.create(event_name=name, pub_date=pub_date, end_date=end_date)


class EventModelTest(TestCase):

    def test_can_register_before_pubdate(self):
        pub_date = timezone.now() + datetime.timedelta(days=1)
        end_date = pub_date + datetime.timedelta(days=1)
        future_event = Event(event_name="Future Event", pub_date=pub_date, end_date=end_date)
        self.assertFalse(future_event.can_register())

    def test_can_register_in_register_date(self):
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = pub_date + datetime.timedelta(days=2)
        register_event = Event(event_name="Register Event", pub_date=pub_date, end_date=end_date)
        self.assertTrue(register_event.can_register())

    def test_can_register_after_end_date(self):
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = pub_date + datetime.timedelta(hours=20)
        old_event = Event(event_name="Old Event", pub_date=pub_date, end_date=end_date)
        self.assertFalse(old_event.can_register())

    def test_is_expired_before_pubdate(self):
        pub_date = timezone.now() + datetime.timedelta(days=1)
        end_date = pub_date + datetime.timedelta(days=1)
        future_event = Event(event_name="Future Event", pub_date=pub_date, end_date=end_date)
        self.assertFalse(future_event.is_expired())

    def test_is_expired_in_register_date(self):
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = pub_date + datetime.timedelta(days=2)
        register_event = Event(event_name="Register Event", pub_date=pub_date, end_date=end_date)
        self.assertFalse(register_event.is_expired())

    def test_is_expired_after_end_date(self):
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = pub_date + datetime.timedelta(hours=20)
        old_event = Event(event_name="Old Event", pub_date=pub_date, end_date=end_date)
        self.assertTrue(old_event.is_expired())

    def test_event_name(self):
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = pub_date + datetime.timedelta(days=2)
        register_event = Event(event_name="Register Event", pub_date=pub_date, end_date=end_date)
        self.assertEqual(str(register_event), "Register Event")
