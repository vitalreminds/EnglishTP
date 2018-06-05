from django.db import models
from django.contrib.auth.models import User
from registration.models import Teacher, Alumn
from django.contrib.auth import get_user_model
from .validators import validate_file_extension



# Create your models here.


class Group1(models.Model):
    name = models.CharField(max_length=20, verbose_name='NombreGrupo')
    alumn = models.ManyToManyField(Alumn, blank=True, verbose_name='Alumnos')
    teacher = models.ForeignKey(Teacher, verbose_name='Profesor', on_delete=models.CASCADE)

    class Meta:
        verbose_name='Grupo'
        verbose_name_plural='Grupos'

    def __str__(self):
        return self.name

class Exercise(models.Model):
    group = models.ForeignKey(Group1, verbose_name='Grupo', on_delete=models.CASCADE)
    user = get_user_model()
    title = models.CharField(max_length=40, verbose_name='Titulo')
    teacher = models.ForeignKey(Teacher,verbose_name='Autor', on_delete=models.CASCADE)
    """
    alumns = models.ManyToManyField(Profile, verbose_name='Alumnos') 
    """
    date_delivery = models.DateTimeField(verbose_name='Fecha de entrega')
    url = models.FileField(verbose_name='Url', upload_to='Exercises', validators=[validate_file_extension])
    created = models.DateTimeField( auto_now_add=True ,verbose_name='Fecha de creacion')
    updated = models.DateTimeField( auto_now=True ,verbose_name='Fecha de actualizacion')

    class Meta:
        verbose_name = 'Ejecicio'
        verbose_name_plural = 'Ejercicios'
        ordering = ['-created']

    def get_time_value(self):
        year = str(self.date_delivery.year)
        month = str(self.date_delivery.month)
        day = str(self.date_delivery.day)
        
        if len(month) == 1:
            month = "0"+month
        if len(day) == 1:
            day = "0"+day


        return year+"-"+month+"-"+day

    def __str__(self):
        return self.title
