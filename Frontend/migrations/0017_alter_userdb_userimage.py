# Generated by Django 3.2.10 on 2023-08-23 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0016_reviewdb_userimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdb',
            name='UserImage',
            field=models.ImageField(blank=True, default='avatar1.png', null=True, upload_to='profile_images'),
        ),
    ]
