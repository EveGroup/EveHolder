"""This module contains views of the website."""
from django.shortcuts import render


def home(request):
    return render(request, 'accounts/dashboard.html')


def event(request):
    return render(request, 'accounts/event.html')


def visitor(request):
    return render(request, 'accounts/visitor.html')
