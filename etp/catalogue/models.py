from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from registration.models import Profile
from .validators import validate_file_extension

# Create your models here.


class Book(models.Model):
    user = get_user_model()
    title = models.CharField(max_length=40, verbose_name='Titulo')
    description = RichTextField(verbose_name="Descripcion")
    provider = models.ForeignKey(user, null=True, on_delete=models.CASCADE)
    autor = models.CharField(max_length=40,verbose_name='Autor')
    quantity = models.IntegerField(verbose_name='Cantidad', default=0)
    edition = models.IntegerField(verbose_name='Edicion')
    editorial = models.CharField(max_length=40, verbose_name='Editorial' )
    cover_page = models.ImageField(verbose_name='Portada',upload_to="Profiles", null=True, blank=True, validators=[validate_file_extension])
    price = models.FloatField(verbose_name='Precio')
    client = models.ManyToManyField(Profile, verbose_name='Cliente')
    ISBN = models.CharField(max_length=15, verbose_name='ISBN')
    created = models.DateTimeField( auto_now_add=True ,verbose_name='Fecha de creacion')
    updated = models.DateTimeField( auto_now=True ,verbose_name='Fecha de actualizacion')


    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['-created']

    def __str__(self):
        return self.title