# Generated by Django 3.2.10 on 2023-08-18 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0004_usermessagesdb'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBookingDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserName', models.CharField(blank=True, max_length=100, null=True)),
                ('MovieName', models.CharField(blank=True, max_length=200, null=True)),
                ('ScreenName', models.CharField(blank=True, max_length=200, null=True)),
                ('ShowName', models.CharField(blank=True, max_length=200, null=True)),
                ('SelectedDate', models.DateField(blank=True, null=True)),
                ('NoOfSeats', models.IntegerField(blank=True, null=True)),
                ('SeatType', models.CharField(blank=True, max_length=50, null=True)),
                ('SeatNumbers', models.CharField(blank=True, max_length=5, null=True)),
                ('PaymentStatus', models.CharField(blank=True, max_length=5, null=True)),
                ('BookedDate', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
