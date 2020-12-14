"""Module for testing visitor account."""

from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse

from eve_holder.tests.test_event_models import create_event
from eve_holder.models import Event, Visitor


class VisitorTests(TestCase):
    """Class for testing everything about visitor."""

    def setUp(self) -> None:
        """Set up visitor."""
        # create user to pair with Visitor account
        self.user = User.objects.create_user("visitor", "test@gmail.com", "testPassword")
        # create group name 'Visitor'
        Group.objects.create(name='Visitor')
        # add user to Visitor group
        visitor_group = Group.objects.get(name='Visitor')
        visitor_group.user_set.add(self.user)
        # create visitor pairing with user
        self.visitor = Visitor.objects.create(user=self.user, name='visitor')

        self.event1 = create_event(name='event1', duration=1)
        self.event2 = create_event(name='event2', duration=1)
        self.event3 = create_event(name='event3', duration=1)

        self.client.login(username='visitor', password='testPassword')

    def test_visitor_access_to_host_pages(self):
        """Account type 'Visitor' must not be able to visit any host pages."""
        url = reverse('eve_holder:host')
        response = self.client.get(url)
        event_id = Event.objects.get(event_name=self.event1.event_name).id
        self.assertContains(response, "You are not authorize to view the page!")
        url = reverse('eve_holder:delete_event', args=(event_id,))
        response = self.client.get(url)
        self.assertContains(response, "You are not authorize to view the page!")
        url = reverse('eve_holder:create_event')
        response = self.client.get(url)
        self.assertContains(response, "You are not authorize to view the page!")
        url = reverse('eve_holder:edit_event', args=(event_id,))
        response = self.client.get(url)
        self.assertContains(response, "You are not authorize to view the page!")
        url = reverse('eve_holder:visitors_list', args=(event_id,))
        response = self.client.get(url)
        self.assertContains(response, "You are not authorize to view the page!")
        url = reverse('eve_holder:information', args=(event_id,))
        response = self.client.get(url)
        self.assertContains(response, "You are not authorize to view the page!")

    def test_delete_account(self):
        """Test delete account."""
        # create new visitor
        user = User.objects.create_user("delete", "test@gmail.com", "testPassword")
        visitor_group = Group.objects.get(name='Visitor')
        visitor_group.user_set.add(user)
        visitor_to_be_deleted = User.objects.filter(username='delete')
        v = visitor_group.user_set.filter(username='delete')
        self.assertQuerysetEqual(visitor_to_be_deleted, ['<User: delete>'])
        self.assertQuerysetEqual(v, ['<User: delete>'])
        # delete visitor
        visitor_to_be_deleted.delete()
        u = User.objects.filter(username='delete')
        v = visitor_group.user_set.filter(username='delete')
        self.assertQuerysetEqual(u, [])
        self.assertQuerysetEqual(v, [])

    def test_visitor_registered_events_page(self):
        """registered_events_page should show all events that are registered."""
        self.visitor.event.add(self.event1)
        url = reverse('eve_holder:visitor_registered_events')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['events'], ['<Event: event1>'])

    def test_visitor_events_page(self):
        """Events page should have all the event not include events that already registered."""
        self.client.login(username='visitor', password='testPassword')
        self.visitor.event.add(self.event1)
        url = reverse('eve_holder:events')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['events'], ['<Event: event3>', '<Event: event2>'], ordered=False)

    def test_event_is_removed_from_events_page_after_join(self):
        """Visitor name should not appear in event visitor list when the event is cancelled."""
        event = Event.objects.get(event_name='event1')
        url = reverse('eve_holder:events')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['events'], ['<Event: event3>', '<Event: event2>', '<Event: event1>'],
                                 ordered=False)
        self.visitor.event.add(event)
        url = reverse('eve_holder:events')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['events'], ['<Event: event3>', '<Event: event2>'], ordered=False)

    # prob with visitor_set
    def test_cancel_event(self):
        """Visitor name should not appear in event visitor list when the event is cancelled."""
        event = Event.objects.get(event_name='event1')
        self.assertQuerysetEqual(event.visitor_set.all(), [])
        self.visitor.event.add(event)
        self.assertQuerysetEqual(event.visitor_set.all(), ['<Visitor: visitor>'])
        self.visitor.event.remove(event)
        self.assertQuerysetEqual(event.visitor_set.all(), [])

    #

    def test_events_page_contain_cancelled_event(self):
        """When visitor cancel the event, events page should display it."""
        event = Event.objects.get(event_name='event1')
        self.assertQuerysetEqual(event.visitor_set.all(), [])
        self.visitor.event.add(event)
        self.assertQuerysetEqual(event.visitor_set.all(), ['<Visitor: visitor>'])
        self.visitor.event.remove(event)
        self.assertQuerysetEqual(event.visitor_set.all(), [])
        url = reverse('eve_holder:events')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['events'], ['<Event: event3>', '<Event: event2>', '<Event: event1>']
                                 , ordered=False)

    def test_join_event(self):
        """Visitor name should appear in event visitor list."""
        event = Event.objects.get(event_name='event1')
        self.visitor.event.add(event)
        self.assertQuerysetEqual(event.visitor_set.all(), ['<Visitor: visitor>'])

    def test_visitor_in_visitor_set_removed_after_account_is_deleted(self):
        """The name of the visitor who deletes their account should not appear in visitor_set."""
        user = User.objects.create_user("test", "test@gmail.com", "testPassword")
        visitor_group = Group.objects.get(name='Visitor')
        visitor_group.user_set.add(user)
        test_visitor = Visitor.objects.create(user=user, name='test_visitor')
        event = Event.objects.get(event_name='event1')
        test_visitor.event.add(event)
        self.assertQuerysetEqual(event.visitor_set.all(), ['<Visitor: test_visitor>'])
        user.delete()
        self.assertQuerysetEqual(event.visitor_set.all(), [])
