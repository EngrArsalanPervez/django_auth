from django import forms
from django.contrib.auth.models import User


class CustomLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Username',
        'class': 'form-control',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))


class CustomRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Username',
        'class': 'form-control',
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter Email',
        'class': 'form-control',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat Password',
        'class': 'form-control',
    }))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Additional validation logic if needed
        return cleaned_data


class CustomUpdateEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter Email',
        'class': 'form-control',
    }))
