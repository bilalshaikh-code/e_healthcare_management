# forms.py
from django import forms
from .models import CustomUser

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['image', 'email', 'first_name', 'last_name', 'address','mobile_number']  # Example fields, adjust as needed
