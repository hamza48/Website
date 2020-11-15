from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
        #Leave as empty string for base url
	path('', views.home, name="home"),
	path('register', views.register, name="register"),
]