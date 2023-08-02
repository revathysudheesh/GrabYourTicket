from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    phone_number=models.CharField(max_length=15,blank=True, null=True)
    profile_image=models.ImageField(upload_to='ProfileImages', null=True, blank=True)

