from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import ClientForm



def home(request):
    context = {}
    return render(request, 'home/main.html')




def register(request):
    if request.method == 'POST':  # data sent by user
        form = ClientForm(request.POST)
        if form.is_valid():
            mail = form.clean_user_mail()
            psw = form.clean_user_password()
            user = authenticate(username=mail, password=psw)
            if user is not None:
                login(request, user)
                print("User is valid, active and authenticated")
                return render(request, 'home/register.html')
            # A backend authenticated the credentials
            else:

                print("Username or password are incorrect")
                messages.error(request, 'Username or Password are incorrect !')
                return redirect('home')
    else :
        return render(request, 'home/main.html')



