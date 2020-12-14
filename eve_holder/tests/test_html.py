"""Module for testing rendering html."""

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from eve_holder.models import Event, Visitor, Host
from eve_holder.tests.test_event_models import create_event


class HtmlTests(TestCase):

    def setUp(self) -> None:
        """Set up visitor and host."""
        # for visitor
        user = User.objects.create_user("visitor", "test@gmail.com", "testPassword")
        Group.objects.create(name='Visitor')
        visitor_group = Group.objects.get(name='Visitor')
        visitor_group.user_set.add(user)
        self.visitor = Visitor.objects.create(user=user)
        self.event1 = create_event(name='event1', duration=1)

        # for host
        user2 = User.objects.create_user("host", "test@gmail.com", "testPassword")
        Group.objects.create(name='Host')
        host_group = Group.objects.get(name='Host')
        host_group.user_set.add(user2)
        self.host = Host.objects.create(user=user2)
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
        self.assertTemplateUsed(response, 'eve_holder/visitors/events.html')

    def test_render_visitor_join_event_page(self):
        """Should render eve_holder/join_event.html"""
        self.client.login(username='visitor', password='testPassword')
        url = reverse('eve_holder:event_register', args=(self.event1_id,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'eve_holder/visitors/join_event.html')

    # test render for host
    def test_render_host_my_account_page(self):
        """Should render eve_holder/hosts/host_my_account.html."""
        self.client.login(username='host', password='testPassword')
        url = reverse('eve_holder:my_account')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'eve_holder/hosts/host_my_account.html')

    def test_render_host_page(self):
        """Should render eve_holder/hosts/host.html."""
        self.client.login(username='host', password='testPassword')
        url = reverse('eve_holder:host')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'eve_holder/hosts/host.html')

    def test_render_create_event(self):
        """Should render eve_holder/hosts/create_event.html."""
        self.client.login(username='host', password='testPassword')
        url = reverse('eve_holder:create_event')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'eve_holder/hosts/create_event.html')

    def test_render_edit_event(self):
        """Should render eve_holder/hosts/create_event.html."""
        self.client.login(username='host', password='testPassword')
        url = reverse('eve_holder:edit_event', args=(self.event1_id,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'eve_holder/hosts/create_event.html')

    def test_render_delete_event(self):
        """Should redirect to host page."""
        self.client.login(username='host', password='testPassword')
        url = reverse('eve_holder:delete_event', args=(self.event1_id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('eve_holder:host'))

    def test_render_visitor_list(self):
        """Should render eve_holder/visitors/visitors_list.html."""
        self.client.login(username='host', password='testPassword')
        url = reverse('eve_holder:visitors_list', args=(self.event1_id,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'eve_holder/hosts/visitors_list.html')

    # render for both host and visitor
    def test_render_event_detail(self):
        """Should render eve_holder/events/event_detail.html."""
        event = create_event(name='new_event', duration=3)
        event.event_host.add(self.host)
        self.client.login(username='host', password='testPassword')
        url = reverse('eve_holder:event_detail', args=(event.pk,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'eve_holder/hosts/host_event_detail.html')
        self.client.logout()
        self.client.login(username='visitor', password='testPassword')
        url = reverse('eve_holder:event_detail', args=(event.pk,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'eve_holder/host_and_visitor/event_detail.html')

    def test_render_delete_account(self):
        """Should redirect to homepage."""
        self.client.login(username='visitor', password='testPassword')
        response = self.client.post(reverse('eve_holder:delete_account'), HTTP_REFERER=reverse('eve_holder:homepage'))
        self.assertRedirects(response, reverse('eve_holder:homepage'))
        self.client.login(username='host', password='testPassword')
        response = self.client.post(reverse('eve_holder:delete_account'), HTTP_REFERER=reverse('eve_holder:homepage'))
        self.assertRedirects(response, reverse('eve_holder:homepage'))
