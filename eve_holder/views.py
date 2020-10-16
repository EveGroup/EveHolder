"""This module contains views of the website."""
from django.http import HttpResponse


def index(request):
    """Class that handle the index page in html."""
    return HttpResponse("Hello, world. You're at the polls index.")
