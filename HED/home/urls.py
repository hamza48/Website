from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
        #Leave as empty string for base url
	path('', views.home, name="home"),
	path('loggin', views.logginUser, name="logginUser"),
	path('logout',views.logout, name = 'logout'),
	path('profile', views.profile, name = 'profile'),
	path('register', views.register, name = 'register'),
]