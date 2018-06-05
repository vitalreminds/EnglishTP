from django.db import models
from .validators import validate_file_extension


# Create your models here.

class YoutubeVideo(models.Model):
    title = models.CharField(null=True, max_length=40, verbose_name='Titulo')
    views = models.CharField(null=True,max_length=12, verbose_name='Vistas')
    duration = models.CharField(null=True,max_length=12, verbose_name='Duracion')
    videoId = models.CharField(max_length=12, verbose_name='VideoId')
    letter = models.FileField(upload_to='letters', validators=[validate_file_extension])
    words = models.FileField(upload_to='words', validators=[validate_file_extension])
    
    class Meta:
        verbose_name='YoutubeVideo'
        verbose_name_plural='YoutubeVideos'

    def __str__(self):
        return self.title