from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    phone_number=models.IntegerField(blank=True, null=True)
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
    TheatreImage = models.ImageField(upload_to='TheatreImages', null=True, blank=True)

class ScreenDB(models.Model):
    ScreenName = models.CharField(max_length=200, null=True, blank=True)
    ScreenCapacity = models.IntegerField(null=True, blank=True)
    PremiumCapacity=models.IntegerField(null=True, blank=True)
    StandardCapacity=models.IntegerField(null=True, blank=True)
    ScreenStatus= models.CharField(max_length=200, null=True, blank=True)
class MovieDB(models.Model):
    MovieName = models.CharField(max_length=200, null=True, blank=True)
    MovieLanguage = models.CharField(max_length=200, null=True, blank=True)
    MovieGenre = models.CharField(max_length=200, null=True, blank=True)
    MoviePoster = models.ImageField(upload_to='MoviePoster', null=True, blank=True)
    MoviePoster1 = models.ImageField(upload_to='MoviePoster', null=True, blank=True)
    MoviePoster2 = models.ImageField(upload_to='MoviePoster', null=True, blank=True)
    MoviePoster3 = models.ImageField(upload_to='MoviePoster', null=True, blank=True)
    MovieType = models.CharField(max_length=2, null=True, blank=True)
    MovieSynopsis = models.CharField(max_length=500, null=True, blank=True)
    MovieDuration= models.CharField(max_length=10, null=True, blank=True)
    MovieRelease = models.DateField(max_length=10, null=True, blank=True)
    MovieTrailer = models.CharField(max_length=500, null=True, blank=True)
    MovieStatus=models.CharField(max_length=10, null=True, blank=True)
    MovieActor1Name=models.CharField(max_length=30, null=True, blank=True)
    MovieActor1Image = models.ImageField(upload_to='Actors', null=True, blank=True)
    MovieActor2Name = models.CharField(max_length=30, null=True, blank=True)
    MovieActor2Image = models.ImageField(upload_to='Actors', null=True, blank=True)
    MovieActor3Name = models.CharField(max_length=30, null=True, blank=True)
    MovieActor3Image = models.ImageField(upload_to='Actors', null=True, blank=True)
    MovieActor4Name = models.CharField(max_length=30, null=True, blank=True)
    MovieActor4Image = models.ImageField(upload_to='Actors', null=True, blank=True)
    MovieActor5Name = models.CharField(max_length=30, null=True, blank=True)
    MovieActor5Image = models.ImageField(upload_to='Actors', null=True, blank=True)
    MovieCrew1Name = models.CharField(max_length=30, null=True, blank=True)
    MovieCrew1Role = models.CharField(max_length=30, null=True, blank=True)
    MovieCrew1Image = models.ImageField(upload_to='Crew', null=True, blank=True)
    MovieCrew2Name = models.CharField(max_length=30, null=True, blank=True)
    MovieCrew2Role = models.CharField(max_length=30, null=True, blank=True)
    MovieCrew2Image = models.ImageField(upload_to='Crew', null=True, blank=True)
    MovieCrew3Name = models.CharField(max_length=30, null=True, blank=True)
    MovieCrew3Role = models.CharField(max_length=30, null=True, blank=True)
    MovieCrew3Image = models.ImageField(upload_to='Crew', null=True, blank=True)
    MovieCrew4Name = models.CharField(max_length=30, null=True, blank=True)
    MovieCrew4Role = models.CharField(max_length=30, null=True, blank=True)
    MovieCrew4Image = models.ImageField(upload_to='Crew', null=True, blank=True)
    MovieCrew5Name = models.CharField(max_length=30, null=True, blank=True)
    MovieCrew5Role = models.CharField(max_length=30, null=True, blank=True)
    MovieCrew5Image = models.ImageField(upload_to='Crew', null=True, blank=True)

class ShowTimeDB(models.Model):
    ShowTimeName=models.CharField(max_length=200, null=True, blank=True)
    MovieName = models.CharField(max_length=200, null=True, blank=True)
    ScreenName = models.CharField(max_length=200, null=True, blank=True)
    StartTime= models.CharField(max_length=20,null=True, blank=True)
    EndTime= models.CharField(max_length=20,null=True, blank=True)
    Date = models.DateField(null=True, blank=True)
    PriceStandard= models.IntegerField(null=True, blank=True)
    TotalStandardTickets= models.IntegerField(null=True, blank=True)
    AvailableStandardTickets=models.IntegerField(null=True, blank=True)
    PricePremium = models.IntegerField(null=True, blank=True)
    TotalPremiumTickets = models.IntegerField(null=True, blank=True)
    AvailablePremiumTickets = models.IntegerField(null=True, blank=True)
    Status = models.CharField(max_length=200, null=True, blank=True)

class SeatingDB(models.Model):
    ShowTimeName=models.CharField(max_length=200, null=True, blank=True)
    ScreenName=models.CharField(max_length=200, null=True, blank=True)
    SeatClass=models.CharField(max_length=200, null=True, blank=True)
    SeatNumber=models.CharField(max_length=5, null=True, blank=True)
    Date= models.DateField(null=True, blank=True)
    Status=models.CharField(max_length=20, null=True, blank=True)











