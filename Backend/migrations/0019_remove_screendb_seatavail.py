# Generated by Django 3.2.10 on 2023-08-12 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0018_auto_20230812_2041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='screendb',
            name='SeatAvail',
        ),
    ]