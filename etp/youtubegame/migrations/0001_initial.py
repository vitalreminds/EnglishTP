# Generated by Django 2.0.2 on 2018-06-04 03:14

from django.db import migrations, models
import youtubegame.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YoutubeVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, null=True, verbose_name='Titulo')),
                ('views', models.CharField(max_length=12, null=True, verbose_name='Vistas')),
                ('duration', models.CharField(max_length=12, null=True, verbose_name='Duracion')),
                ('videoId', models.CharField(max_length=12, verbose_name='VideoId')),
                ('letter', models.FileField(upload_to='letters', validators=[youtubegame.validators.validate_file_extension])),
                ('words', models.FileField(upload_to='words', validators=[youtubegame.validators.validate_file_extension])),
            ],
            options={
                'verbose_name': 'YoutubeVideo',
                'verbose_name_plural': 'YoutubeVideos',
            },
        ),
    ]
