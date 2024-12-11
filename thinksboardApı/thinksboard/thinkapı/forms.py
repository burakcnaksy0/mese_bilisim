from .models import *
from django import forms


class UserLogInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserLogInModel
        fields = "__all__"


class DevicesListForm(forms.Form):
    DEVICE_CHOICES = [
        ("1", "https://thingsboard.cloud/api/device/95cf0970-a5b2-11ef-af8e-935e87032cca"),
        ("2", "https://thingsboard.cloud/api/device/cd3c12f0-a69c-11ef-9126-e7e15310409e"),
        ("3", "https://thingsboard.cloud/api/device/ea345690-a6fd-11ef-8300-7376affecafe"),
        ("4", "https://thingsboard.cloud/api/device/e03eb710-a730-11ef-af8e-935e87032cca"),
        ("5", "https://thingsboard.cloud/api/device/87a23920-abe9-11ef-ba27-0bc777b49120"),
        ("6", "https://thingsboard.cloud/api/device/dab4ae41-b3c8-11ef-8d27-31960e941324"),
    ]
    device = forms.ChoiceField(choices=DEVICE_CHOICES)
