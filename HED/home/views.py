from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
import datetime
from .models import Commande,Client
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from enum import Enum




#### Messages returned by views to html files ########

NO_ACCOUNT_FOUND           = """Aucun compte n'existe avec l'email saisi, cliquez sur s'inscrire et créez un nouveau compte"""
USERNAME_OR_PASSWORD_WRONG = """ email et/ou le mot de pass sont incorrect"""
TOKEN_IS_WRONG             = """le code de verification saisi n'est pas correcte, réessayez"""
PASSWORDS_ARENT_EQUALS     = """Attention ! : Les mots de passe saisis ne sont pas identiques"""
EMAIL_ALREADY_EXIST        = """Un compte avec cet email existe deja, cliquez sur connexion pour vous connectez """
TOKEN_IS_RIGHT             = " Félicitations ! Votre compte a bien été activé, vous pouvez maintenant vous connectez"

########### Macros definition  #########

def TOKEN_RESENDED(user_mail) :
    stringOfTokenResended = " Un nouveau code  a été renvoyé à l'adresse mail "+user_mail+ \
                                " saisissez le"
    return stringOfTokenResended

def TOKEN_SENDED(user_mail)  :
    stringOfTokenSended = "le code de verification a été envoyé à l'adresse mail "+user_mail+\
                          " cliquez sur Connexion pour le saisir "
    return stringOfTokenSended

############# Enum ######################
#/* State of order to be followed */
class StateOfOrder(Enum):
    ToBeConfirmed = 0
    Confirmed     = 1
    ToBeDelivred  = 2
    Delivred      = 3
    Canceled      = 4

# /* Types of service that HED provides*/
class TypesOfServices(Enum):
    Pharmacy = "Pharmacy"
    Food     = "Food"
    Gift     = "Gift"
    Race     = "Race"
    Service  = "Service"
    Home     = "Home"


# /* Views */
@login_required
def resend_token(request):
    context = {}
    user_loggedin = request.user
    user_loggedin.client.generator_token = randint(10000000, 99999999)
    user_loggedin.save()
    subject = 'Nouveau code d'"'inscription'"
    message = f'Bonjour {user_loggedin.first_name},\n '\
              f'Vous nous avez demandé d'' envoyer un nouveau code pour compléter votre inscription sur notre plateforme de livraison HED, \n ' \
              f'votre nouveau code pour confirmer votre inscription est : {user_loggedin.client.generator_token}. \n'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_loggedin.email, ]
    context = {
        "user_mail": user_loggedin.email,
    }
    send_mail(subject, message, email_from, recipient_list)
    print(user_loggedin.client.generator_token)
    messages.error(request, TOKEN_RESENDED(user_loggedin.email))
    return render(request,'home/confirmRegistration.html',context)



def home(request):
    context = {}
    logout(request)
    # This check is made to  logged out the user when he request home
    return render(request, 'home/main.html', context)

@login_required
def Pharmacy(request):
    user_session = request.user
    user_session.client.service = TypesOfServices.Pharmacy
    print(user_session.client.service)
    user_session.save()
    context = {}
    return render(request, 'home/Pharmacie.html', context)

###############################################################
# This class "logout"  to loggout a user,No treatement needed #
###############################################################

def logout_view(request):
    context = {}
    logout(request)
    return redirect('home')


######################  LOGGED_IN  ###################################
#                           @Info                                    #
# This view is made to display user interface after a login          #
# This view must be accessible only for user loggedIn                #
######################################################################
                                                                     #
@login_required                                                      #
def logged_in(request):                                              #
    context = {}                                                     #
    return render(request, 'home/register.html', context)            #
                                                                     #
##################### END OF LOGGED_IN VIEW  #########################



######################  tokent_display ######################################
#                           @Info                                           #
# This view is made to display for user an interface to confirm             #
# his registration                                                          #
# if user is verified and request this view we redirect him to              #
# logged_in view                                                            #
# This view must be accessible only for user loggedIn                       #
#############################################################################
                                                                            #
@login_required                                                             #
def token_display(request):                                                 #
    context = {}                                                            #
    user_loggedin = request.user                                            #
    if(user_loggedin.client.mail_verified == True):                         #
        return redirect ('logged_in')                                       #
    else:                                                                   #
        return render(request, 'home/confirmRegistration.html', context)    #
                                                                            #
################## END OF token_display view ################################




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
    context = {}
    if request.method == 'POST':  # data sent by user
        email = request.POST['email']
        psw = request.POST['psw']
        if User.objects.filter(email=email).exists():
            client_object = User.objects.get(email=email)
            if(client_object.client.pswRegistration == psw):
                    user = authenticate(request, username=client_object.username,
                                        password=client_object.client.pswRegistration)
                    if user is not None:
                        login(request, user)
                        if(client_object.client.mail_verified):
                            return redirect('logged_in')
                        else:
                            return redirect('token_display')

                    else:
                        messages.error(request, NO_ACCOUNT_FOUND)
                        return redirect('home')
            else :
                messages.error(request, USERNAME_OR_PASSWORD_WRONG)
        else :
            messages.error(request, NO_ACCOUNT_FOUND)

    return redirect('home')


###########################################################
# This class "profile" is made to display for the user    #
# his informations, orders , or to let him loggout          #
###########################################################
@login_required
def profile(request):
        current_user = request.user
        context = {
            "first_name" : current_user.first_name,
            "last_name"  : current_user.last_name,
            "email"      : current_user.email,
            "telephone"  : current_user.client.Telephone,
            "Adresse"    : current_user.client.adresse
        }
        #note = Note.objects.create(id = None, owner=current_user, Type= "Test")
        #note.save()
        #print(note.owner.first_name)
        #print(note.Type)
        #print(current_user.note.Type)
        return render(request, 'home/profile.html', context)

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
        adresse = request.POST['adresse']
        ville = request.POST['city']
        complementAdresse = request.POST['moreInfo']
        codePostale = request.POST['zipCode']
        user = request.user
        user.client.Telephone = mobile_phone
        user.client.adresse = adresse
        user.client.ville = ville
        user.client.codePostale = codePostale
        user.client.complementAdresse = complementAdresse
        user.save()
        return redirect('profile')


###########################################################
# This class "register" is made to register new user      #
# if no user with the same mail already exist.            #
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
            user = User.objects.create_user(username=username, password=pswRegistration1,
                                            email=emailRegistration,
                                            first_name=First_name, last_name=Last_name)
            user.client.mail_verified = False
            # Generate a random token
            user.client.generator_token = randint(10000000,99999999)
            user.date_joined = datetime.date.today()
            user.client.pswRegistration = pswRegistration1
            user.save()
            ##The Mail that will be sent to the user###
            subject = 'Confirmation d'"'inscription sur HED'"
            message = f'Hi {user.first_name}, thank you for registering in HED, \n ' \
                      f'your  key to confirm your registration is {user.client.generator_token}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            #user.save()
            messages.error(request, TOKEN_SENDED(user.email))
            return redirect('home')
    else:
        return redirect('home')



@login_required
def Verify_token(request):
    context = {}
    user_loggedin = request.user
    if request.method == 'POST':  # data sent by user
        token_input = request.POST['token']
    token_generated = user_loggedin.client.generator_token
    if(token_generated == token_input):
        user_loggedin.client.mail_verified = True
        user_loggedin.save()
        messages.error(request, TOKEN_IS_RIGHT)
        return redirect('logged_in')
    else:
        messages.error(request, TOKEN_IS_WRONG)
        return render(request, 'home/ConfirmRegistration.html', context)




##############################################################
# This class "addingItem" is made to add items on user Cart  #
##############################################################
@login_required
def addingItem(request):
        current_user = request.user
        context = {}
        service = current_user.client.service
        commande = Commande.objects.create(user=current_user, service=service,
                                           date=datetime.datetime.now(),
                                           status=StateOfOrder.ToBeConfirmed ,
                                           price=0, delivery_man= "")
        commande.save()
        return redirect('Pharmacy')


##############################################################
# This class "myOrders" shows orders of user(TBC,Done,...)   #
##############################################################
@login_required
def myOrders(request):
        current_user = request.user
        context = {}
        service = current_user.client.service


        return redirect('Pharmacy')

##############  END OF FILE   #####################


