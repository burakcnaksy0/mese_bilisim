from django import forms
from .models import *


class MyForm(forms.Form):
    name = forms.CharField(label="Ad")
    email = forms.EmailField(label="E-posta")
    message = forms.CharField(label="Mesaj", widget=forms.Textarea)


class LoginUser(forms.Form):
    username = forms.CharField(label="username")
    surname = forms.CharField(label="surname")
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    email = forms.EmailField(label="E-posta")
    message = forms.CharField(label="Mesaj", widget=forms.Textarea)


class İnstagram(forms.Form):
    name = forms.CharField(label="name")
    surname = forms.CharField(label="surname")
    username = forms.CharField(label="username")
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    email = forms.EmailField(label="email")


class Movie(forms.Form):
    name = forms.CharField(label="Name")
    year = forms.DateField(label="Year")
    topic = forms.CharField(label="Topic")
    message = forms.CharField(label="Message")
    image = forms.ImageField(label="İmage")


class MovieForm(forms.ModelForm):
    class Meta:
        model = MovieApp
        fields = ["name", "year", "topic", "message", "image"]
