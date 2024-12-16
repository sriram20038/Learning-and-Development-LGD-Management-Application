from django import forms
from .models import User

class Login_form(forms.Form): 
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class Signup_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['name','email','password','confirm_password','role']


