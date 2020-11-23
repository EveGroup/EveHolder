"""Module for creating forms."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateTimeField, ModelForm

from .models import *


class EventForm(ModelForm):
    # CharField.widget.attrs['readonly'] = True
    pub_date = DateTimeField(widget=forms.widgets.DateTimeInput(format="%Y-%m-%d %H:%M:%S"))
    end_date = DateTimeField(widget=forms.widgets.DateTimeInput(format="%Y-%m-%d %H:%M:%S"))

    # event_host = CharField()

    class Meta:
        model = Event
        fields = '__all__'
        # fields = ['event_name', 'event_description', 'pub_date', 'end_date']
        # exclude = ['event_host']

    # def __init__(self, *args, **kwargs):
    #     self.Meta.fields['event_host'].queryset = Host.objects.filter(id=args[0].id)
    #     super(EventForm, self).__init__(*args, **kwargs)


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
        # groups = 'Visitors'
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'groups']




class EventRegistrationForm(ModelForm):
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
