"""Module for creating forms"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateTimeField, ModelForm, CharField

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
    class Meta:
        model = User
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
