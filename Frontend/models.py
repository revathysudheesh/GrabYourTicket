from django.db import models

# Create your models here.
class UserDB(models.Model):
    UserName=models.CharField(max_length=100, null=True, blank=True)
    UserEmail= models.EmailField(max_length=200, null=True, blank=True)
    UserContact= models.IntegerField(null=True, blank=True)
    UserPassword=models.CharField(max_length=100, null=True, blank=True)
class ReviewDB(models.Model):
    UserName=models.CharField(max_length=100, null=True, blank=True)
    Review=models.CharField(max_length=500, null=True, blank=True)
    Date=models.DateField(null=True,blank=True)
    MovieName=models.CharField(max_length=200, null=True, blank=True)

class UserMessagesDB(models.Model):
    Name=models.CharField(max_length=100, null=True, blank=True)
    Email=models.EmailField(max_length=100, null=True, blank=True)
    Subject=models.CharField(max_length=100, null=True, blank=True)
    Message=models.CharField(max_length=500, null=True, blank=True)
    PostDate=models.DateField(null=True,blank=True)

