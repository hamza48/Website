from django.shortcuts import render


def home(request):
    context = {}
    return render(request, 'home/main.html', context)