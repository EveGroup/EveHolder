"""Module for creating forms."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import *


class EventForm(ModelForm):
    event_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        "placeholder": "Event Name...",
        "style": "border: none; outline: none; background: none; line-height: 25px; border-bottom: 1px solid black;"
                 "border-radius: 0px"
    }))
    event_description = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        "placeholder": "Event description...",
        "style": "border: none; outline: none; background: none; line-height: 25px; border-bottom: 1px solid black;"
                 "border-radius: 0px"
    }))

    event_location = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        "placeholder": "Event Location...",
        "style": "border: none; outline: none; background: none; line-height: 25px; border-bottom: 1px solid black;"
                 "border-radius: 0px"
    }))

    pub_date = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "date",
        "style": "line-height: 25px; margin-top: -10px; font-size: 10px; border: none; outline: none; background: none;"
                 "border-bottom: 1px solid black; border-radius: 0px"
    }))

    end_date = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "date",
        "style": "font-size: 10px; line-height: 25px; margin-top: -10px; border: none; outline: none; background:"
                 "none; border-bottom: 1px solid black; border-radius: 0px"
    }))

    event_date = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "date",
        "style": "line-height: 25px; margin-top: -10px; border: none; outline: none; background: none;"
                 "border-bottom: 1px solid black; border-radius: 0px",
    }))

    amount_accepted = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control input my-3",
        "type": "text",
        "placeholder": "Amount accepted...",
        "style": "line-height: 25px; margin-top: -10px; border: none; outline: none; background: none;"
                 "border-bottom: 1px solid black; border-radius: 0px"
    }))

    class Meta:
        model = Event
        fields = ['event_name', 'event_description', 'event_location', 'amount_accepted', 'pub_date', 'event_date',
                  'end_date']
        # exclude = ['event_host']


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
        'style': 'font-size: 16px; padding: 5px; display: inline-block; margin-top: -5px; margin-left: 2.3%;'
                 'border: none; border-radius: 5px; color: #031b88; text-align: center; height: 30px; '
                 'width: 450px; background-color: rgba(173,186,211,0.4)'
    }), label="name: ")

    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "email",
        'style': 'font-size: 16px; padding: 5px; display: inline-block; margin-top: -5px; margin-left: 2.3%;'
                 'border: none; border-radius: 5px; color: #031b88; text-align: center; height: 30px; '
                 'width: 450px; background-color: rgba(173,186,211,0.4)'
    }), label="Email: ")

    phone_num = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        'style': 'font-size: 16px; padding: 5px; display: inline-block; margin-top: -5px; margin-left: 2.3%;'
                 'border: none; border-radius: 5px; color: #031b88; text-align: center; height: 30px; '
                 'width: 450px; top: -10px; background-color: rgba(173,186,211,0.4)'
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
