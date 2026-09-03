from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):

    name = forms.CharField(
        max_length=100,
        required=True
    )

    email = forms.EmailField(
        required=True
    )

    phone_no = forms.CharField(
        max_length=15,
        required=True
    )

    class Meta:
        model = CustomUser

        fields = [
            'name',
            'username',
            'email',
            'phone_no',
            'password1',
            'password2',
        ]