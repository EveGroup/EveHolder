"""Module for tests auth."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    """Class for testing authorization."""

    def setUp(self) -> None:
        """Set up user."""
        # self.host = User.objects.create_user("Host", "test@gmail.com", "testPassword")
        # self.visitor = User.objects.create_user("Visitor", "test@gmail.com", "testPassword")
        self.admin = User.objects.create_user("admin", "test@gmail.com", "testPassword")

    def test_admin_access_to_host(self):
        """User without group name 'Host' must not be able to access to any page for host."""
        self.client.login(username='admin', password='testPassword')
        url = reverse('eve_holder:host')
        response = self.client.get(url)
        self.assertContains(response, "You are not authorize to view the page!")

    def test_admin_access_to_visitor(self):
        """User without group name 'Visitor' must not be able to access to any page for visitor."""
        self.client.login(username='admin', password='testPassword')
        url = reverse('eve_holder:events')
        response = self.client.get(url)
        self.assertContains(response, "You are not authorize to view the page!")



