# Generated by Django 3.2.10 on 2023-08-05 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0004_actordb_crewdb_moviedb'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moviedb',
            name='MovieActor',
        ),
        migrations.RemoveField(
            model_name='moviedb',
            name='MovieCrew',
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieActor1Image',
            field=models.ImageField(blank=True, null=True, upload_to='Actors'),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieActor1Name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieActor2Image',
            field=models.ImageField(blank=True, null=True, upload_to='Actors'),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieActor2Name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieActor3Image',
            field=models.ImageField(blank=True, null=True, upload_to='Actors'),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieActor3Name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieActor4Image',
            field=models.ImageField(blank=True, null=True, upload_to='Actors'),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieActor4Name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieActor5Image',
            field=models.ImageField(blank=True, null=True, upload_to='Actors'),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieActor5Name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieCrew1Image',
            field=models.ImageField(blank=True, null=True, upload_to='Actors'),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieCrew1Name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieCrew1Role',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieCrew2Name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieCrew2Role',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieCrew3Image',
            field=models.ImageField(blank=True, null=True, upload_to='Actors'),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieCrew3Name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieCrew3Role',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieCrew4Image',
            field=models.ImageField(blank=True, null=True, upload_to='Actors'),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieCrew4Name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieCrew4Role',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieCrew5Image',
            field=models.ImageField(blank=True, null=True, upload_to='Actors'),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieCrew5Name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='MovieCrew5Role',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.DeleteModel(
            name='ActorDB',
        ),
        migrations.DeleteModel(
            name='CrewDB',
        ),
    ]
