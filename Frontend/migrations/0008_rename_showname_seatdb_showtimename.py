# Generated by Django 3.2.10 on 2023-08-18 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0007_auto_20230818_1436'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seatdb',
            old_name='ShowName',
            new_name='ShowTimeName',
        ),
    ]
