from django import forms
from django.forms import ModelForm
from .models import Task, Profile


class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Add in a new task"}))

    class Meta:
        model = Task
        fields = ["title","content","completed",]
        exclude = ["user",]


class UpdateProfileForm(forms.ModelForm):
    profile_img = forms.ImageField(label="Profile image", required=False, widget=forms.FileInput(attrs={"class":"form-control-file"}))

    class Meta:
        model = Profile
        fields = ["profile_img",]
        exclude = ["user",]



