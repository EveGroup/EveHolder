"""Module for creating forms."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.forms import ModelForm

from .models import *


class EventForm(ModelForm):
    event_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        "placeholder": "Event Name...",
        "style": "border: none; outline: none; background: none; line-height: 25px; border-bottom: 1px solid black;"
                 "border-radius: 0px; border-color: #ffffff; color: #ffffff"
    }))
    event_description = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        "placeholder": "Event description...",
        "style": "border: none; outline: none; background: none; line-height: 25px; border-bottom: 1px solid black;"
                 "border-radius: 0px; border-color: #ffffff; color: #ffffff"
    }))

    event_location = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        "placeholder": "Event Location...",
        "style": "border: none; outline: none; background: none; line-height: 25px; border-bottom: 1px solid black;"
                 "border-radius: 0px; border-color: #ffffff; color: #ffffff"
    }))

    pub_date = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "date",
        "style": "line-height: 25px; margin-top: -10px; font-size: 10px; border: none; outline: none; background: none;"
                 "border-bottom: 1px solid black; border-radius: 0px; border-color: #ffffff; color: #ffffff"
    }))

    end_date = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "date",
        "style": "font-size: 10px; line-height: 25px; margin-top: -10px; border: none; outline: none; background:"
                 "none; border-bottom: 1px solid black; border-radius: 0px;border-color: #ffffff; color: #ffffff"
    }))

    event_date = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "date",
        "style": "line-height: 25px; margin-top: -10px; border: none; outline: none; background: none;"
                 "border-bottom: 1px solid black; border-radius: 0px; border-color: #ffffff; color: #ffffff",
    }))

    amount_accepted = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control input my-3",
        "type": "text",
        "placeholder": "Amount accepted...",
        "style": "line-height: 25px; margin-top: -10px; border: none; outline: none; background: none;"
                 "border-bottom: 1px solid black; border-radius: 0px; border-color: #ffffff; color: #ffffff"
    }))

    event_image = forms.ClearableFileInput(attrs={
        'class': 'form-control',
        'style': 'color: #ffffff'
    })

    class Meta:
        model = Event
        fields = ['event_name', 'event_description', 'event_location', 'amount_accepted', 'pub_date', 'event_date',
                  'end_date', 'event_image']


class RegisterForm(forms.Form):
    profile_pic = forms.ImageField()


class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "autofocus": True,
        "class": "form__input",
        "id": "username",
        "placeholder": "Username",
        "type": "text"
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        "autofocus": True,
        "class": "form__input",
        "id": "email",
        "placeholder": "Email Address",
        "type": "text"
    }), label="Email: ")
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "autofocus": True,
        "class": "form__input",
        "id": "first_name",
        "placeholder": "First Name",
        "type": "text"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "autofocus": True,
        "class": "form__input",
        "id": "last_name",
        "placeholder": "Last Name",
        "type": "text"
    }))
    password1 = forms.CharField(widget=forms.TextInput(attrs={
        "autofocus": True,
        "class": "form__input",
        "id": "password1",
        "placeholder": "Password",
        "type": "text"
    }))
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        "autofocus": True,
        "class": "form__input",
        "id": "password2",
        "placeholder": "Confirm Password",
        "type": "text"
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'groups']


class EventRegistrationForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        "placeholder": "Username...",
        'style': 'font-size: 16px; padding: 5px; display: inline-block; margin-top: -5px; margin-left: 2.3%;'
                 'border: none; border-radius: 5px; color: #031b88; text-align: center; height: 30px; '
                 'width: 450px; background-color: rgba(173,186,211,0.4)'
    }), label="name: ")

    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "email",
        "placeholder": "Email...",
        'style': 'font-size: 16px; padding: 5px; display: inline-block; margin-top: -5px; margin-left: 2.3%;'
                 'border: none; border-radius: 5px; color: #031b88; text-align: center; height: 30px; '
                 'width: 450px; background-color: rgba(173,186,211,0.4)'
    }), label="Email: ")

    phone_num = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        "placeholder": "Phone number...",
        'style': 'font-size: 16px; padding: 5px; display: inline-block; margin-top: -5px; margin-left: 2.3%;'
                 'border: none; border-radius: 5px; color: #031b88; text-align: center; height: 30px; '
                 'width: 450px; top: -10px; background-color: rgba(173,186,211,0.4)'
    }), label="phone: ")

    class Meta:
        model = Visitor
        fields = ['name', 'phone_num', 'email']


class UpdateInformationUserForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        'style': 'font-size: 16px; padding: 5px; display: inline-block; margin-top: -5px;'
                 'border: none; border-radius: 5px; color: #ffffff; text-align: left; height: 30px;'
                 'top: -10px; background-color: rgba(255, 255, 255,0.1)'
    }), label="First name: ")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        'style': 'font-size: 16px; padding: 5px; display: inline-block; margin-top: -5px;'
                 'border: none; border-radius: 5px; color: #ffffff; text-align: left; height: 30px;'
                 'top: -10px; background-color: rgba(255, 255, 255,0.1)'
    }), label="Last name: ")

    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        'style': 'font-size: 16px; padding: 5px; display: inline-block; margin-top: -5px;'
                 'border: none; border-radius: 5px; color: #ffffff; text-align: left; height: 30px;'
                 'top: -10px; background-color: rgba(255, 255, 255,0.1)'
    }), label="Email: ")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UpdateInformationVisitorForm(ModelForm):
    phone_num = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "number",
        "min": '1',
        'style': 'font-size: 16px; padding: 5px; display: inline-block; margin-top: -5px;'
                 'border: none; border-radius: 5px; color: #ffffff; text-align: left; height: 30px;'
                 'top: -10px; background-color: rgba(255, 255, 255,0.1)'
    }), label="Phone number: ")

    profile_pic = forms.ImageField()

    class Meta:
        model = Visitor
        fields = ['phone_num', 'profile_pic']


class UpdateInformationHostForm(ModelForm):
    phone_num = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input form-control my-3",
        "type": "text",
        "min": '1',
        'style': 'font-size: 16px; padding: 5px; display: inline-block; margin-top: -5px;'
                 'border: none; border-radius: 5px; color: #ffffff; text-align: left; height: 30px;'
                 'top: -10px; background-color: rgba(255, 255, 255,0.1)'
    }), label="Phone number: ")

    profile_pic = forms.ImageField()

    class Meta:
        model = Host
        fields = ['phone_num', 'email', 'profile_pic']
