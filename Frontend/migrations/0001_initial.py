# Generated by Django 3.2.10 on 2023-08-16 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserEmail', models.EmailField(blank=True, max_length=200, null=True)),
                ('UserContact', models.IntegerField(blank=True, null=True)),
                ('UserPassword', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
