# Generated by Django 3.2.10 on 2023-08-16 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0022_moviedb_movietrailer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviedb',
            name='MoviePoster1',
            field=models.ImageField(blank=True, null=True, upload_to='MoviePoster1'),
        ),
    ]
