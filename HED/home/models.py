from django.db import models
from django import forms
# Create your models here.


class Client(models.Model):
    emailRegistration = models.CharField(max_length=200)
    pswRegistration1 = models.CharField(max_length=200)
    pswRegistration2 = models.CharField(max_length=200)
    First_name = models.CharField(max_length=200)
    Last_name = models.CharField(max_length=200)



