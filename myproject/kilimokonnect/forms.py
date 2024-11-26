from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import User


class User(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('owner', 'Owner'),
        ('retailer', 'Retailer')
    )

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.Select)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    location = forms.CharField(max_length=255)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['user_type', 'first_name', 'last_name', 'email', 'location', 'password1', 'password2']