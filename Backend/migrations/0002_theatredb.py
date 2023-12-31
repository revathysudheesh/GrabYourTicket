# Generated by Django 3.2.10 on 2023-08-04 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TheatreDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TheatreName', models.CharField(blank=True, max_length=200, null=True)),
                ('TheatreAddress', models.CharField(blank=True, max_length=500, null=True)),
                ('TheatreContact', models.CharField(blank=True, max_length=20, null=True)),
                ('TheatreWebsite', models.CharField(blank=True, max_length=200, null=True)),
                ('TheatreEmail', models.EmailField(blank=True, max_length=200, null=True)),
                ('TheatreCapacity', models.IntegerField(blank=True, null=True)),
                ('TheatreScreen', models.IntegerField(blank=True, null=True)),
                ('TheatreStatus', models.CharField(blank=True, max_length=200, null=True)),
                ('TheatreImage', models.ImageField(blank=True, null=True, upload_to='TheatreImages')),
            ],
        ),
    ]
