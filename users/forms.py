from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False)
    referral_code = forms.CharField(max_length=36, required=False,
                                    label='Referral Code (optional)')


    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'phone_number',
                  'password1', 'password2')
