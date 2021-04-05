from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from enum import Enum
# Create your models here.


#/* State of order to be followed */
class StateOfOrder(Enum):
    ToBeConfirmed = 0
    Confirmed     = 1
    ToBeDelivred  = 2
    Delivred      = 3
    Canceled      = 4

# /* Types of service that HED provides*/
class TypesOfServices(Enum):
    Pharmacy = "Pharmacy"
    Food     = "Food"
    Gift     = "Gift"
    Race     = "Race"
    Service  = "Service"
    Home     = "Home"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pswRegistration     = models.CharField(max_length=200)
    generator_token      = models.CharField(max_length=8)
    service              = models.CharField(max_length=20,
                                            choices=[(tag, tag.value) for tag in TypesOfServices],
                                            default=TypesOfServices.Home)
    mail_verified        = models.BooleanField(default=False)
    sexe                 = models.CharField(max_length=30, default= "NULL")
    adresse              = models.CharField(max_length=400, default="")
    Telephone            = models.CharField(max_length=10, default="")
    ville                = models.CharField(max_length=30, default="")
    codePostale          = models.IntegerField(default=0)
    complementAdresse    = models.CharField(max_length=100, default="")
    Date_of_registration = models.DateField(blank=True, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Client.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.client.save()





class Commande(models.Model):
    # user other fields
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    service      = models.CharField(max_length=20,
                                    choices=[(tag, tag.value) for tag in TypesOfServices],
                                    default=TypesOfServices.Home)
    date         = models.DateTimeField(blank=True, null=True)
    status       = models.CharField(max_length=30,
                                    choices=[(tag, tag.value) for tag in StateOfOrder],
                                    default=StateOfOrder.ToBeConfirmed)
    price        = models.IntegerField(default=0)
    delivery_man = models.CharField(max_length= 40)

