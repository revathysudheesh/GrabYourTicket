# Generated by Django 3.2.10 on 2023-08-18 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0005_userbookingdb'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.CharField(max_length=5)),
                ('status', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('showtime', models.CharField(max_length=100)),
            ],
        ),
    ]
