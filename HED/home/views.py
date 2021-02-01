from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import Client
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
import datetime



NO_ACCOUNT_FOUND = """Aucun compte n'existe avec l'email saisi !"""
USERNAME_OR_PASSWORD_WRONG = """ email et/ou le mot de pass sont incorrecte"""
TOKEN_IS_WRONG = """le code de verification saisi n'est pas correcte, réessayez"""
PASSWORDS_ARENT_EQUALS = """Les mot de passes ne sont pas identiques"""
EMAIL_ALREADY_EXIST = """L'email saisi existe deja """


def home(request):
    context = {}
    # This check is made to  logged out the user when he request home
    return render(request, 'home/main.html', context)


###############################################################
# This class "logout"  to loggout a user,No treatement needed #
###############################################################


def logout(request):
    logout(request)
    return render(request, 'home/main.html')





###########################################################
# This class "register" is made to fetch user's input     #
# in order to login him if he has an account              #
# it calls ClientForm from forms.py file                  #
###########################################################
def logginUser(request):
    if request.method == 'POST':  # data sent by user
        email = request.POST['email']
        psw = request.POST['psw']
        if User.objects.filter(email=email).exists():
            client_object = User.objects.get(email=email)
            if(client_object.client.pswRegistration == psw):
                if(client_object.client.mail_verified):
                    user = authenticate(request, username=client_object.username, password=client_object.client.pswRegistration)
                    if user is not None:
                        login(request, user)
                        context = {
                            "first_name": client_object.first_name,
                        }
                        return render(request, 'home/register.html', context)
                    else:
                        messages.error(request, NO_ACCOUNT_FOUND)
                        return render(request, 'home/main.html')
                    # Return an 'invalid login' error message.

                else:
                    request.session['token'] = client_object.client.generator_token
                    return render(request, 'home/confirmRegistration.html')
            else :
                messages.error(request, USERNAME_OR_PASSWORD_WRONG)
        else :
            messages.error(request, NO_ACCOUNT_FOUND)
    else :
        return render(request, 'home/main.html')

###########################################################
# This class "profile" is made to display for the user    #
# his informations, orders , or to let him loggout          #
###########################################################
def profile(request):
    current_user = request.user
    context = {
        "first_name" : current_user.first_name,
        "last_name"  : current_user.last_name,
        "email"      : current_user.email,
        "telephone"  : current_user.client.Telephone,
        "Adresse"    : current_user.client.adresse
    }
    return render(request, 'home/profile.html', context)
###########################################################
# This class "inscription" is made to fetch user's input  #
# in order to register him if no user with the same mail  #
# already exist.                                          #
# it calls ClientRegistrationForm from forms.py file      #
###########################################################


def register(request):
    passwordAreCorrect = False
    emailIsNotUsed = False

    context = {
        "user_mail": "",
    }
    if request.method == 'POST':  # data sent by user
        emailRegistration = request.POST['emailRegistration']
        pswRegistration1 = request.POST['pswRegistration1']
        pswRegistration2 = request.POST['pswRegistration2']
        First_name = request.POST['prenom']
        Last_name = request.POST['nom']


        if pswRegistration1 != pswRegistration2:
            passwordAreCorrect = False
            messages.error(request, PASSWORDS_ARENT_EQUALS)
            return render(request, 'home/main.html', context)
        else :
            passwordAreCorrect = True

        if User.objects.filter(email=emailRegistration).exists():
            messages.error(request, EMAIL_ALREADY_EXIST)
            emailIsNotUsed = False
            return render(request, 'home/main.html', context)
        else :
            emailIsNotUsed = True

        if(passwordAreCorrect & emailIsNotUsed) :
            username = Last_name + First_name
            user = User.objects.create_user(username = username,password = pswRegistration1 , email = emailRegistration,
                                            first_name = First_name, last_name = Last_name)
            user.client.mail_verified = False
            user.client.generator_token = randint(10000000,99999999)
            user.date_joined = datetime.date.today()
            user.client.pswRegistration = pswRegistration1
            user.save()
            subject = 'Confirmation d''inscription sur HED'
            message = f'Hi {user.first_name}, thank you for registering in HED, \n ' \
                      f'your  key to confirm your registration is {user.client.generator_token}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            context = {
                "user_mail": user.email,
            }
            send_mail(subject, message, email_from, recipient_list)
            user.save()
            return render(request, 'home/main.html', context)
    else:
        context = {
            "user_mail": "",
        }
        return render(request, 'home/main.html', context)


##############  END OF FILE   #####################


def Verify_token(request):
    if request.method == 'POST':  # data sent by user
        token_input = request.POST['token']
    current_user = request.user
    if(current_user.client.generator_token == token_input):

        current_user.client.mail_verified = True
        current_user.save()
        context = {
            "token_verified" : current_user.client.mail_verified,
        }
    else:
        context = {
            "token_verified": "",
        }
        messages.error(request, TOKEN_IS_WRONG)

    return render(request, 'home/main.html', context)





