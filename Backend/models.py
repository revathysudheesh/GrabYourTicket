from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    phone_number=models.CharField(max_length=15,blank=True, null=True)
    profile_image=models.ImageField(upload_to='ProfileImages', null=True, blank=True)
class TheatreDB(models.Model):
    TheatreName = models.CharField(max_length=200, null=True, blank=True)
    TheatreAddress = models.CharField(max_length=500, null=True, blank=True)
    TheatreContact = models.CharField(max_length=20, null=True, blank=True)
    TheatreWebsite = models.CharField(max_length=200, null=True, blank=True)
    TheatreEmail = models.EmailField(max_length=200, null=True, blank=True)
    TheatreCapacity = models.IntegerField(null=True, blank=True)
    TheatreScreen = models.IntegerField(null=True, blank=True)
    TheatreStatus = models.CharField(max_length=200, null=True, blank=True)
    TheatreImage=models.ImageField(upload_to='TheatreImages', null=True, blank=True)

