# Generated by Django 3.2.10 on 2023-08-05 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0002_theatredb'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScreenDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ScreenName', models.CharField(blank=True, max_length=200, null=True)),
                ('ScreenCapacity', models.IntegerField(blank=True, null=True)),
                ('SeatAvail', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]