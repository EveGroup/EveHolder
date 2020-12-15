"""Module for testing visitor account."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from eve_holder.tests.test_event_models import create_event
from eve_holder.models import Event, Host, Visitor


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
        self.host = Host.objects.create(user=self.user, name='host')
        self.event1 = create_event(name='event1', duration=1)
        self.polar_bear_event = create_event(name='polar bear sight-seeing', duration=1)
        self.visit_museum = create_event(name='museum', duration=1)

        self.client.login(username='host', password='testPassword')

        # create group for visitor
        Group.objects.create(name='Visitor')

    def test_host_access_to_visitor_pages(self):
        """Account type 'Host' must not be able to visit any visitor pages."""
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
        url = reverse('eve_holder:close_notification', args=(event_id,))
        response = self.client.get(url)
        self.assertContains(response, "You are not authorize to view the page!")

    def test_events_of_host(self):
        """Test host's events."""
        self.polar_bear_event.event_host.add(self.host)
        self.visit_museum.event_host.add(self.host)
        self.assertQuerysetEqual(self.host.event_set.all(), ['<Event: polar bear sight-seeing>',
                                                             '<Event: museum>'], ordered=False)
        self.assertQuerysetEqual(Event.objects.all(), ['<Event: polar bear sight-seeing>', '<Event: museum>',
                                                       '<Event: event1>'], ordered=False)

    def test_host_delete_account(self):
        """Host can delete account."""
        self.assertQuerysetEqual(Host.objects.all(), ['<Host: host>'])
        self.host.delete()
        self.assertQuerysetEqual(Host.objects.all(), [])

    def test_event_removed_after_delete_account(self):
        """All events that belong to deleted host should be removed."""
        # create host to be deleted
        user = User.objects.create_user("deleteme", "test@gmail.com", "testPassword")
        host_group = Group.objects.get(name='Host')
        host_group.user_set.add(user)
        Host.objects.create(user=user, name='delete')
        self.polar_bear_event.event_host.add(self.host)
        self.visit_museum.event_host.add(self.host)
        self.assertQuerysetEqual(self.host.event_set.all(), ['<Event: polar bear sight-seeing>',
                                                             '<Event: museum>'], ordered=False)
        self.client.post(reverse('eve_holder:delete_account'), HTTP_REFERER=reverse('eve_holder:homepage'))
        self.assertQuerysetEqual(Event.objects.all(), ['<Event: event1>'])

    def test_my_events_page(self):
        """my events page should show only events that created by host who is logging in."""
        self.polar_bear_event.event_host.add(self.host)
        self.visit_museum.event_host.add(self.host)
        respond = self.client.get(reverse('eve_holder:host'))
        self.assertQuerysetEqual(respond.context['events'], ['<Event: polar bear sight-seeing>',
                                                             '<Event: museum>'], ordered=False)

    def test_visitor_list(self):
        """Visitor list page shows all participated visitors."""
        user1 = User.objects.create_user("visitor1", "test@gmail.com", "testPassword")
        visitor_group = Group.objects.get(name='Visitor')
        visitor_group.user_set.add(user1)
        visitor1 = Visitor.objects.create(user=user1, name='visitor1')

        user2 = User.objects.create_user("visitor2", "test@gmail.com", "testPassword")
        visitor_group = Group.objects.get(name='Visitor')
        visitor_group.user_set.add(user2)
        visitor2 = Visitor.objects.create(user=user2, name='visitor2')

        user3 = User.objects.create_user("visitor3", "test@gmail.com", "testPassword")
        visitor_group = Group.objects.get(name='Visitor')
        visitor_group.user_set.add(user3)
        visitor3 = Visitor.objects.create(user=user3, name='visitor3')

        self.assertQuerysetEqual(Visitor.objects.all(),
                                 ['<Visitor: visitor1>', '<Visitor: visitor2>', '<Visitor: visitor3>'], ordered=False)
        event = Event.objects.get(id=self.polar_bear_event.pk)
        # visitor3 is not added
        event.visitor_set.add(visitor1, visitor2)
        respond = self.client.get(reverse('eve_holder:visitors_list', args=(event.id,)))
        self.assertQuerysetEqual(respond.context['visitor_registered_events'],
                                 ['<Visitor: visitor1>', '<Visitor: visitor2>'], ordered=False)
