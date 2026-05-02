from .base.forms import BaseCustomUserCreationForm, BaseCustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import TextInput, PasswordInput
from django import forms
from django.contrib.auth import get_user_model


class CustomUserCreationForm(BaseCustomUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Password*"
        self.fields["password2"].label = "Confirm password*"
        self.fields.pop("usable_password", None)



class CustomUserChangeForm(BaseCustomUserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].disabled = True  # ← makes it readonly

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "first_name", "last_name", "tel"]
        exclude = ["password1", "password2",]


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
