from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import Client

from .forms import ClientForm
from .forms import ClientRegistrationForm


def home(request):
    context = {}
    return render(request, 'home/main.html')


###############################################################
# This class "logout"  to loggout a user,No treatement needed #
###############################################################

def logout(request):
    django_logout(request)
    return render(request, 'home/main.html')


###########################################################
# This class "profile" is made to display for the user    #
# his informations, orders , or to let him loggout          #
###########################################################

def profile(request):
    context = {}
    return render(request, 'home/profile.html')


###########################################################
# This class "register" is made to fetch user's input     #
# in order to login him if he has an account              #
# it calls ClientForm from forms.py file                  #
###########################################################

def logginUser(request):
    if request.method == 'POST':  # data sent by user
        email = request.POST['email']
        psw = request.POST['psw']
        if Client.objects.filter(emailRegistration=email).exists():
            client_object = Client.objects.get(emailRegistration=email)
            if(client_object.pswRegistration1 == psw):
                context = {
                    "first_name": client_object.First_name
                }
                return render(request, 'home/register.html', context)
                #return HttpResponseNotFound("You're connected MTF")
            else :
                return render(request, 'home/main.html')
        else :
            print("No User with this email is founded ")

    return render(request, 'home/main.html')


###########################################################
# This class "inscription" is made to fetch user's input  #
# in order to register him if no user with the same mail  #
# already exist.                                          #
# it calls ClientRegistrationForm from forms.py file      #
###########################################################


def register(request):
    if request.method == 'POST':  # data sent by user
        emailRegistration = request.POST['emailRegistration']
        pswRegistration1 = request.POST['pswRegistration1']
        pswRegistration2 = request.POST['pswRegistration2']
        First_name = request.POST['prenom']
        Last_name = request.POST['nom']

        if pswRegistration1 != pswRegistration2:
            passwordAreCorrect = False
            return HttpResponseNotFound("Your passwords are wrong !")
        else :
            passwordAreCorrect = True

        if Client.objects.filter(emailRegistration=emailRegistration).exists():
            return HttpResponseNotFound("This email is already in use !")
            emailIsNotUsed = False
        else :
            emailIsNotUsed = True

        if(passwordAreCorrect & emailIsNotUsed) :
            new_client = Client(emailRegistration=emailRegistration, pswRegistration1=pswRegistration1,
                                pswRegistration2=pswRegistration2, First_name=First_name, Last_name=Last_name)
            new_client.save()
    return render(request, 'home/main.html')



##############  END OF FILE   #####################