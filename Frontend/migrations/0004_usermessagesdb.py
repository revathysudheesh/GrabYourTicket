# Generated by Django 3.2.10 on 2023-08-16 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0003_reviewdb'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMessagesDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=100, null=True)),
                ('Email', models.EmailField(blank=True, max_length=100, null=True)),
                ('Subject', models.CharField(blank=True, max_length=100, null=True)),
                ('Message', models.CharField(blank=True, max_length=500, null=True)),
                ('PostDate', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
