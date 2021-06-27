from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
        #Leave as empty string for base url
	path('',              views.home,           name="home"			 ),
	url('logged_in',      views.logged_in, 		name="logged_in"	 ),
	url('UpdateUserInfo', views.UpdateUserInfo, name="UpdateUserInfo"),
	path('loggin', 		  views.logginUser, 	name="logginUser"	 ),
	path('Pharmacy', 	  views.Pharmacy, 	    name='Pharmacy'	 	 ),
	path('logout_view',	  views.logout_view, 	name='logout_view'	 ),
	path('profile', 	  views.profile, 		name='profile'		 ),
	path('register', 	  views.register, 		name='register'		 ),
	path('resend_token',  views.resend_token,  name='resend_token'	 ),
	path('Verify_token',  views.Verify_token,  name='Verify_token'	 ),
	url('token_display',  views.token_display, name='token_display'  ),
	url('addingItem', 	  views.addingItem,    name='addingItem'     ),
	url('myOrders',       views.myOrders,      name='myOrders'       ),
	url('Test',           views.test,          name='Test'           ),
]