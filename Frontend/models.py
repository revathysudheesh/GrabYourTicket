from django.db import models

# Create your models here.
class UserDB(models.Model):
    UserName=models.CharField(max_length=100, null=True, blank=True)
    UserEmail= models.EmailField(max_length=200, null=True, blank=True)
    UserContact= models.IntegerField(null=True, blank=True)
    UserPassword=models.CharField(max_length=100, null=True, blank=True)
    UserImage=models.ImageField(upload_to="profile_images",null=True,blank=True,default='avatar1.png')
    UserFirstName=models.CharField(max_length=100, null=True, blank=True)
    UserLastName=models.CharField(max_length=100, null=True, blank=True)
    UserAddress=models.CharField(max_length=500, null=True, blank=True)

class ReviewDB(models.Model):
    UserName=models.CharField(max_length=100, null=True, blank=True)
    Review=models.CharField(max_length=500, null=True, blank=True)
    Date=models.DateField(null=True,blank=True)
    MovieName=models.CharField(max_length=200, null=True, blank=True)
    UserImage=models.ImageField(upload_to="profileImage", null=True, blank=True)

class UserMessagesDB(models.Model):
    Name=models.CharField(max_length=100, null=True, blank=True)
    Email=models.EmailField(max_length=100, null=True, blank=True)
    Subject=models.CharField(max_length=100, null=True, blank=True)
    Message=models.CharField(max_length=500, null=True, blank=True)
    PostDate=models.DateField(null=True,blank=True)

class UserBookingDB(models.Model):
    UserName=models.CharField(max_length=100, null=True, blank=True)
    MovieName=models.CharField(max_length=200, null=True, blank=True)
    ScreenName=models.CharField(max_length=200, null=True, blank=True)
    ShowName=models.CharField(max_length=200, null=True, blank=True)
    SelectedDate=models.DateField(null=True, blank=True)
    NoOfSeats=models.IntegerField(null=True, blank=True)
    SeatNumbers= models.CharField(max_length=5, null=True, blank=True)
    SeatNumberOnly= models.CharField(max_length=5, null=True, blank=True)
    StartTime= models.CharField(max_length=20,null=True, blank=True)
    AmountToBePaid= models.IntegerField(null=True, blank=True)
    PaymentStatus=models.CharField(max_length=5, null=True, blank=True)
    BookedDate=models.DateField(null=True, blank=True)

class SeatDB(models.Model):
    SeatNumber = models.CharField(max_length=5)
    SeatStatus = models.CharField(max_length=20)  # 'available', 'selected', 'booked'
    Date = models.DateField()
    ShowTimeName = models.CharField(max_length=100)
    SeatType= models.CharField(max_length=5, null=True, blank=True)
    RowNumber= models.CharField(max_length=5, null=True, blank=True)
