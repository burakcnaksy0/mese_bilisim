from .models import *
from django import forms


class UserLogInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserLogInModel
        fields = "__all__"


class DevicesListForm(forms.Form):
    DEVICE_CHOICES = [
        ('1', 'Device 1'),
        ('2', 'Device 2'),
        ('3', 'Device 3'),
        ('4', 'Device 4'),
        ('5', 'Device 5'),
        ('6', 'Device 6'),
    ]
    device = forms.ChoiceField(choices=DEVICE_CHOICES)
