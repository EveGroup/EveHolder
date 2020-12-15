"""Module for testing search filter."""
from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse

from eve_holder.tests.test_event_models import create_event
from eve_holder.models import Visitor


class SearchTests(TestCase):
    """Class for testing search."""

    def setUp(self) -> None:
        """Set up events."""
        self.shopping = create_event(name="shopping", duration=1)
        self.shopping_with_goose = create_event(name="shopping with goose", duration=1)

        user = User.objects.create_user("visitor", "test@gmail.com", "testPassword")
        Group.objects.create(name='Visitor')
        visitor_group = Group.objects.get(name='Visitor')
        visitor_group.user_set.add(user)
        self.visitor = Visitor.objects.create(user=user)

    def test_search_for_existing_event(self):
        """Search for existing event."""
        self.client.login(username='visitor', password='testPassword')
        response = self.client.post(reverse('eve_holder:search_event'), {'search': 'shopping'},
                                    HTTP_REFERER=reverse('eve_holder:homepage'))
        self.assertQuerysetEqual(response.context['events'], ['<Event: shopping>', '<Event: shopping with goose>'],
                                 ordered=False)

    def test_search_for_not_existing_event(self):
        """Search for not existing event."""
        self.client.login(username='visitor', password='testPassword')
        response = self.client.post(reverse('eve_holder:search_event'), {'search': 'cooking with sloth'},
                                    HTTP_REFERER=reverse('eve_holder:homepage'))
        self.assertQuerysetEqual(response.context['events'], [])

    def test_search_for_nothing(self):
        """Search for nothing."""
        self.client.login(username='visitor', password='testPassword')
        response = self.client.post(reverse('eve_holder:search_event'), {'search': ''},
                                    HTTP_REFERER=reverse('eve_holder:homepage'))
        self.assertContains(response, "Nothing is searched", status_code=200)
