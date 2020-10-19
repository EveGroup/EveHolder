"""This module contains views of the website."""
from django.http import HttpResponse
from django.shortcuts import render
from .models import Host, Event, Visitor


def home(request):
    """Class that handle the index page in html."""
    return render(request, 'home.html')

def login(request):
    """Class that handle the index page in html."""
    return render(request, 'registration/login.html')

def signup(request):
    """Class that handle the index page in html."""
    return render(request, 'signup.html')
