import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestAuth(TestCase):

    def setUp(self) -> None:
        user = User.objects.create_user('Test', 'test@gmail.com', 'testPassword')

    def test_visitors(self):
        url = reverse('eve_holder:visitors', )
