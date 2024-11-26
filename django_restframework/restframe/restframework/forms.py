from django import forms
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    token = forms.CharField(max_length=1000)
    DEVICE_CHOICES = [
        ("1", "Device 1"),
        ("2", "Device 2"),
        ("3", "Device 3"),
        ("4", "Device 4"),
    ]
    device = forms.ChoiceField(choices=DEVICE_CHOICES, label="Cihaz Seçin")

    def __str__(self):
        return self.username
