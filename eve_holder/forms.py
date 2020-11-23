"""Module for creating forms."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateTimeField, ModelForm, DateTimeInput

from .models import *


class EventForm(ModelForm):

    event_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        "placeholder": "Event Name...",
        "style": "line-height: 30px"
    }))
    event_description = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control",
        "type": "text",
        "placeholder": "Event description...",
        "style": "line-height: 30px; margin-top: -10px"
    }))

    event_location = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control ",
        "type": "text",
        "placeholder": "Event Location...",
        "style": "line-height: 30px; margin-top: -10px"
    }))

    pub_date = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control",
        "type": "datetime-local",
        "style": "line-height: 30px; margin-top: -10px; font-size: 10px"
    }))

    end_date = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control ",
        "type": "datetime-local",
        "style": "font-size: 10px; line-height: 30px; margin-top: -10px;"
    }))

    event_date = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control ",
        "type": "date",
        "style": "line-height: 30px; margin-top: -10px",
    }))

    class Meta:
        model = Event
        fields = ['event_name', 'event_description', 'event_location', 'amount_accepted', 'pub_date', 'event_date', 'end_date']

class CreateUserForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        "placeholder": "Enter username...",
        'style': 'border-color:darkgoldenrod; border-radius: 3px; font-size: 12px; padding: 5px'
    }), label="Username: ")
    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "email",
        "placeholder": "Enter email...",
        'style': 'border-color:darkgoldenrod; border-radius: 3px; font-size: 12px; padding: 5px'
    }), label="Email: ")
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        "placeholder": "Enter First name...",
        'style': 'border-color:darkgoldenrod; border-radius: 3px; font-size: 12px; padding: 5px'
    }), label="First name: ")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        "placeholder": "Enter Last name...",
        'style': 'border-color:darkgoldenrod; border-radius: 3px; font-size: 12px; padding: 5px'
    }), label="Last name: ")
    password1 = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "password",
        "placeholder": "Enter Password...",
        'style': 'border-color:darkgoldenrod; border-radius: 3px; font-size: 12px; padding: 5px'
    }), label="Password: ")
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "password",
        "placeholder": "Confirm Password...",
        'style': 'border-color:darkgoldenrod; border-radius: 3px; font-size: 12px; padding: 5px'
    }), label="Password confirm: ")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'groups']




class EventRegistrationForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        'style': 'font-size: 12px; padding: 5px'
    }), label="name: ")

    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "email",
        'style': 'font-size: 12px; padding: 5px'
    }), label="Email: ")

    phone = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        'style': 'font-size: 12px; padding: 5px'
    }), label="phone: ")

    class Meta:
        model = Visitor
        fields = ['name', 'phone_num', 'email']


class UpdateInformationUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UpdateInformationVisitorForm(ModelForm):
    class Meta:
        model = Visitor
        fields = ['phone_num', 'email']


class UpdateInformationHostForm(ModelForm):
    class Meta:
        model = Host
        fields = ['phone_num', 'email']
