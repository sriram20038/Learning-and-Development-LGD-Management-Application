from django import forms
from django.core.exceptions import ValidationError
from .models import User
from django.core.exceptions import ValidationError

# Login Form
class Login_form(forms.Form): 
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        error_messages={'required': 'Email is required.'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        error_messages={'required': 'Password is required.'}
    )

    # Custom validation to check if email format is valid
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email is required.")
        # You can add additional email format validation if necessary
        return email
    
    # Custom validation for password (you can modify the validation logic as required)
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise ValidationError("Password is required.")
        return password
# Signup Form
class Signup_form(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Create a password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'confirm_password', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'role': forms.Select()
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Password validation: check if password and confirm password match
        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError("Passwords do not match")
        return cleaned_data
