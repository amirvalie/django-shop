from django import forms
from .models import Address
from django.contrib.auth import get_user_model
User=get_user_model()

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user','active_address']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['first_name','last_name','phone','email']
