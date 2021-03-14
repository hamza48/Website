from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt






NO_ACCOUNT_FOUND = """Aucun compte n'existe avec l'email saisi !"""
USERNAME_OR_PASSWORD_WRONG = """ email et/ou le mot de pass sont incorrecte"""
TOKEN_IS_WRONG = """le code de verification saisi n'est pas correcte, réessayez"""
PASSWORDS_ARENT_EQUALS = """Les mot de passes ne sont pas identiques"""
EMAIL_ALREADY_EXIST = """L'email saisi existe deja """


def home(request):
    context = {}
    logout(request)
    # This check is made to  logged out the user when he request home
    return render(request, 'home/main.html', context)

@login_required
def Pharmacy(request):
    user_loggedin = request.user
    context = {}
    return render(request, 'home/Pharmacie.html', context)

###############################################################
# This class "logout"  to loggout a user,No treatement needed #
###############################################################

def logout_view(request):
    context = {}
    logout(request)
    #return redirect('home')
    return render(request, 'home/main.html', context)


@login_required
def logged_in(request):
    context = {}
    return render(request, 'home/register.html', context)





def csrf_failure(request, reason=""):
    ctx = {}
    return render(request,'home/main.html', ctx)

###########################################################
# This class "register" is made to fetch user's input     #
# in order to login him if he has an account              #
# it calls ClientForm from forms.py file                  #
###########################################################

@csrf_exempt
def logginUser(request):
    print("Im in logginUser view")
    context = {}
    if request.method == 'POST':  # data sent by user
        email = request.POST['email']
        psw = request.POST['psw']
        if User.objects.filter(email=email).exists():
            client_object = User.objects.get(email=email)
            if(client_object.client.pswRegistration == psw):
                if(client_object.client.mail_verified):
                    user = authenticate(request, username=client_object.username,
                                        password=client_object.client.pswRegistration)
                    if user is not None:
                        login(request, user)
                        return redirect('logged_in')
                        #return render(request, 'home/register.html', context)
                    else:
                        messages.error(request, NO_ACCOUNT_FOUND)
                        return render(request, 'home/main.html', context)
                        # Return an 'invalid login' error message.

                else:
                    request.session['token'] = client_object.client.generator_token
                    request.session['user_id'] = client_object.id
                    return render(request, 'home/confirmRegistration.html')
            else :
                messages.error(request, USERNAME_OR_PASSWORD_WRONG)
        else :
            messages.error(request, NO_ACCOUNT_FOUND)


    return render(request, 'home/main.html', context)

###########################################################
# This class "profile" is made to display for the user    #
# his informations, orders , or to let him loggout          #
###########################################################
@login_required
def profile(request):
    if request.method == 'POST':  # data sent by user
        current_user = request.user
        context = {
            "first_name" : current_user.first_name,
            "last_name"  : current_user.last_name,
            "email"      : current_user.email,
            "telephone"  : current_user.client.Telephone,
            "Adresse"    : current_user.client.adresse
        }
        print(context)
        return render(request, 'home/profile.html', context)
    else :
        return redirect('home')

###########################################################
# This class "UpdateUserInfo" is made to update user info #
# in order to store all informations about him like mobile#
# phone and adress                                        #
#       #
###########################################################

@login_required
def UpdateUserInfo(request):
    if request.method == 'POST':  # data sent by user
        mobile_phone = request.POST['phone']
        user = request.user
        user.client.Telephone = mobile_phone
        user.save()
        return redirect('logged_in')



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
            # Cannot register a new user with an existing username,
            # so we add a random number to username if found
            if  User.objects.filter(username=username).exists():
                username = username + str(randint(0,100))
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
    token_generated = request.session.get('token')
    user_id      =  request.session.get('user_id')
    if(token_generated == token_input):
        user_object = User.objects.get(id=user_id)
        user_object.client.mail_verified = True
        user_object.save()
        context = {
            "token_verified" : user_object.client.mail_verified,
        }
    else:
        context = {
            "token_verified": "",
        }
        messages.error(request, TOKEN_IS_WRONG)

    return render(request, 'home/main.html', context)





