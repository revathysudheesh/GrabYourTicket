# Generated by Django 3.2.10 on 2023-08-22 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0013_userbookingdb_starttime'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbookingdb',
            name='SeatNumberOnly',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]