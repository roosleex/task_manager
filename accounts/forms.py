from .base.forms import BaseCustomUserCreationForm, BaseCustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import TextInput, PasswordInput
from django import forms


class CustomUserCreationForm(BaseCustomUserCreationForm):
    pass



class CustomUserChangeForm(BaseCustomUserChangeForm):
    pass


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
