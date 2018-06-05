from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group


# Create your models here.

def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.delete()

    return 'profiles/'+filename



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name='Avatar', upload_to=custom_upload_to,null=True,blank=True)
    name = models.CharField(max_length=15, verbose_name='nombre')
    lastname1 = models.CharField(max_length=15, verbose_name='Apellido Paterno')
    lastname2 = models.CharField(max_length=15, verbose_name='Apellido Materno')
    key = models.CharField( max_length=15, verbose_name='Boleta')
    score = models.IntegerField(default=0,verbose_name='Score')
    phone = models.CharField( max_length=10, verbose_name='Telefono')
    

    def __str__(self):
        return self.user.username

class Alumn(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.profile.key + " " + self.user.profile.name + " "+ self.user.profile.lastname1 + " "+self.user.profile.lastname2


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    

    def __str__(self):
        return self.user.username


def has_group(user, group_name): 
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False
