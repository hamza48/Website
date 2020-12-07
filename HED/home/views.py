from django.contrib import messages
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import ClientForm
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect




def home(request):
    context = {}
    return render(request, 'home/main.html')


def logout(request):
    django_logout(request)
    return render(request, 'home/main.html')


def profile(request):
    context = {}
    return render(request, 'home/profile.html')

def register(request):
    if request.method == 'POST':  # data sent by user
        form = ClientForm(request.POST)
        if form.is_valid():
            mail = form.clean_user_mail()
            psw = form.clean_user_password()
            user = authenticate(username=mail, password=psw)
            if user is not None:
                login(request, user)
                return render(request,'home/register.html')
            # A backend authenticated the credentials
            else:

                print("Username or password are incorrect")
                messages.error(request, 'Username or Password are incorrect !')
                return redirect('home')
    else :
        return render(request,'home/main.html')



