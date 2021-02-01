from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
# Create your models here.


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pswRegistration     = models.CharField(max_length=200)
    generator_token      = models.CharField(max_length=8)
    logged_in            = models.BooleanField(default=False)
    mail_verified        = models.BooleanField(default=False)
    sexe                 = models.CharField(max_length=30, default= "NULL")
    adresse              = models.CharField(max_length=400, default="")
    Telephone            = models.CharField(max_length=10, default="")
    Date_of_registration = models.DateField(blank=True, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Client.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.client.save()



