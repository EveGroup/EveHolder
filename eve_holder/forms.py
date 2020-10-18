from django import forms
from .models import *

class Host_forms(forms.ModelForm):
    class Meta:
        model = Host
        fields = [
            'name',
            'password'
        ]
        widgets = {
            'password': forms.PasswordInput()
        }


class Visitor_forms(forms.ModelForm):
    class Meta:
        model = Visitors
        fields = [
            'name',
            'password'
        ]
        widgets = {
            'password': forms.PasswordInput()
        }