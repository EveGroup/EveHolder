"""Module for testing rendering html."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from eve_holder.tests.test_event_models import create_event
from eve_holder.models import Event, Visitor, Host


class HtmlTests(TestCase):

    def setUp(self) -> None:
        """Set up visitor and host."""
        # for visitor
        self.user = User.objects.create_user("visitor", "test@gmail.com", "testPassword")
        Group.objects.create(name='Visitor')
        visitor_group = Group.objects.get(name='Visitor')
        visitor_group.user_set.add(self.user)
        self.visitor = Visitor.objects.create(user=self.user)
        self.event1 = create_event(name='event1', duration=1)

        # for host
        self.user2 = User.objects.create_user("host", "test@gmail.com", "testPassword")
        Group.objects.create(name='Host')
        host_group = Group.objects.get(name='Host')
        host_group.user_set.add(self.user)
        self.host = Host.objects.create(user=self.user)
        self.event2 = create_event(name='event2', duration=1)

        self.event1_id = Event.objects.get(event_name=self.event1.event_name).id
        self.event2_id = Event.objects.get(event_name=self.event2.event_name).id

    # test render for visitor
    def test_render_visitor_myaccount_page(self):
        """Should render eve_holder/visitors/visitor_my_account.html"""
        self.client.login(username='visitor', password='testPassword')
        url = reverse('eve_holder:my_account')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'eve_holder/visitors/visitor_my_account.html')

    def test_render_visitor_registered_events_page(self):
        """Should render eve_holder/visitors/visitor_registered_events.html"""
        self.client.login(username='visitor', password='testPassword')
        url = reverse('eve_holder:visitor_registered_events')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'eve_holder/visitors/visitor_registered_events.html')

    def test_render_visitor_update_information_page(self):
        """Should render eve_holder/visitors/visitor_update_information.html"""
        self.client.login(username='visitor', password='testPassword')
        url = reverse('eve_holder:visitor_update_information')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'eve_holder/visitors/visitor_update_information.html')

    def test_render_visitor_all_events_page(self):
        """Should render eve_holder/events/events.html"""
        self.client.login(username='visitor', password='testPassword')
        url = reverse('eve_holder:events')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'eve_holder/events/events.html')

    def test_render_visitor_join_event_page(self):
        """Should render eve_holder/join_event.html"""
        self.client.login(username='visitor', password='testPassword')
        url = reverse('eve_holder:event_register', args=(self.event1_id,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'eve_holder/join_event.html')

    def test_render_visitor_cancel_event_page(self):
        """Should render eve_holder/events/event_cancel.html"""
        self.client.login(username='visitor', password='testPassword')
        url = reverse('eve_holder:event_cancel', args=(self.event1_id,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'eve_holder/events/event_cancel.html')

    # def test_render_visitor_close_notification_redirect_registered_page(self):
    #     """Should render eve_holder/visitors/visitor_registered_events.html"""
    #     self.client.login(username='visitor', password='testPassword')
    #     url = reverse('eve_holder:close_notification', args=(self.event1_id,))
    #     response = self.client.get(url)
    #     self.assertTemplateUsed(response, 'eve_holder/visitors/visitor_registered_events.html')

    # test render for host
    # def test_render_host_myaccount_page(self):
    #     self.client.login(username='host', password='testPassword')
    #     url = reverse('eve_holder:my_account')
    #     response = self.client.get(url)
    #     self.assertTemplateUsed(response, 'eve_holder/hosts/host_my_account.html')