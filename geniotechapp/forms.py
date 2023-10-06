from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser

class InstructorRegistrationForm(UserCreationForm):
    # Define form fields for instructor registration
    class Meta:
        model = CustomUser
        fields = ['full_name', 'age', 'phone_number', 'email', 'gender', 'country', 'password1', 'password2']

class ParentRegistrationForm(UserCreationForm):
    # Define form fields for parent registration
    class Meta:
        model = CustomUser
        fields = ['full_name', 'age', 'phone_number', 'email', 'gender', 'country', 'password1', 'password2']

class PasswordChangeForm(PasswordChangeForm):
    # Custom password change form
    pass
