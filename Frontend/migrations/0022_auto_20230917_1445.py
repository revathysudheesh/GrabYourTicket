# Generated by Django 3.2.10 on 2023-09-17 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0021_checkoutdb_carddetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkoutdb',
            name='CardDetail',
        ),
        migrations.RemoveField(
            model_name='checkoutdb',
            name='CardName',
        ),
        migrations.RemoveField(
            model_name='checkoutdb',
            name='Cvv',
        ),
        migrations.RemoveField(
            model_name='checkoutdb',
            name='Expiry',
        ),
    ]
