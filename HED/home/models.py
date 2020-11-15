from django.db import models
from django import forms
# Create your models here.


class Client(models.Model):
    email = models.CharField(max_length=200)
    psw = models.CharField(max_length=200)
