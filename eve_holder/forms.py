from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import DateTimeField

from .models import *


class EventForm(ModelForm):
    pub_date = DateTimeField(widget=forms.widgets.DateTimeInput(format="%Y-%m-%d %H:%M:%S"))
    end_date = DateTimeField(widget=forms.widgets.DateTimeInput(format="%Y-%m-%d %H:%M:%S"))
    class Meta:
        model = Event
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'groups']


class EventRegistrationForm(ModelForm):
    class Meta:
        model = Visitor
        fields = ['name', 'phone_num', 'email']
