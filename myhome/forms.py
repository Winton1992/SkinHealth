from django import forms
from .models import  UserProfile
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = ("username", "email")

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'gender', 'address', 'email']

