# Generated by Django 3.2.10 on 2023-08-12 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0017_seatingdb'),
    ]

    operations = [
        migrations.AddField(
            model_name='screendb',
            name='PremiumCapacity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='screendb',
            name='StandardCapacity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='seatingdb',
            name='Date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
