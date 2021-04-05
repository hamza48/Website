from django.forms import ModelForm
from .models import Client
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


###########################################################
# This class  is made to fetch datas from  main html file #                                          #
#  This service is used on logginUser view                #
###########################################################

class ClientForm(forms.Form):
    email = forms.CharField()
    psw = forms.CharField()

    def clean_user_mail(self):
        email = self.cleaned_data['email']
        return email

    def clean_user_password(self):
        psw = self.cleaned_data['psw']
        return psw


###########################################################
# This class  is made to fetch datas from  main html file #                                          #
#  This service is used on inscription view               #
###########################################################

class ClientRegistrationForm(forms.ModelForm):
    nom = forms.CharField()
    prenom = forms.CharField()
    emailRegistration = forms.CharField()
    pswRegistration1 = forms.CharField()
    pswRegistration2 = forms.CharField()

    print("Im in ClientRegistrationForm")


    def clean_user_Lastname(self):
        nom = self.cleaned_data['nom']
        return nom

    def clean_user_Firstname(self):
        prenom = self.cleaned_data['prenom']
        return prenom

    def clean_user_email(self):
        emailRegistration = self.cleaned_data['emailRegistration']
        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=emailRegistration)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return emailRegistration
        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')

    def clean_user_psw_Registration1(self):
        pswRegistration1 = self.cleaned_data['pswRegistration1']
        return pswRegistration1

    def clean_user_psw_Registration2(self):
        pswRegistration2 = self.cleaned_data['pswRegistration2']
        return pswRegistration2


##############  END OF FILE   #####################
