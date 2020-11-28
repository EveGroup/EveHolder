"""Module for testing visitor account."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from eve_holder.tests.test_event_models import create_event
from eve_holder.models import Event, Host


class HostTests(TestCase):
    """Class for testing everything about host."""

    def setUp(self) -> None:
        """Set up host."""
        # create user to pair with host account
        self.user = User.objects.create_user("host", "test@gmail.com", "testPassword")
        # create group name 'Host'
        Group.objects.create(name='Host')
        # add user to Host group
        host_group = Group.objects.get(name='Host')
        host_group.user_set.add(self.user)
        # create host pairing with user
        self.host = Host.objects.create(user=self.user)
        self.event1 = create_event(name='event1', duration=1)

    def test_host_access_to_visitor_pages(self):
        """Account type 'Host' must not be able to visit any visitor pages."""
        self.client.login(username='host', password='testPassword')
        url = reverse('eve_holder:visitor_registered_events')
        response = self.client.get(url)
        self.assertContains(response, "You are not authorize to view the page!")
        url = reverse('eve_holder:events')
        response = self.client.get(url)
        self.assertContains(response, "You are not authorize to view the page!")
        url = reverse('eve_holder:visitor_update_information')
        response = self.client.get(url)
        self.assertContains(response, "You are not authorize to view the page!")
        event_id = Event.objects.get(event_name=self.event1.event_name).id
        url = reverse('eve_holder:event_register', args=(event_id,))
        response = self.client.get(url)
        self.assertContains(response, "You are not authorize to view the page!")
        url = reverse('eve_holder:event_cancel', args=(event_id,))
        response = self.client.get(url)
        self.assertContains(response, "You are not authorize to view the page!")
        url = reverse('eve_holder:close_notification', args=(event_id,))
        response = self.client.get(url)
        self.assertContains(response, "You are not authorize to view the page!")

