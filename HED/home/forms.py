from django.forms import ModelForm
from .models import Client
from django import forms
from django.contrib.auth import authenticate

class ClientForm(forms.Form):
        email = forms.CharField()
        psw = forms.CharField()

        def clean_user_mail(self):
            email = self.cleaned_data['email']
            return email

        def clean_user_password(self):
            psw = self.cleaned_data['psw']
            return psw




