from django.shortcuts import render


def register(request):
    context = {}
    return render(request, 'register/registeration.html', context)


from django.shortcuts import render

# Create your views here.
