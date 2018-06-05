from django.contrib import admin
from .models import Exercise, Group1

# Register your models here.
class ExerciseConfig(admin.ModelAdmin):
    readonly_fields = ('created','updated')

class Group1Config(admin.ModelAdmin):
    pass

admin.site.register(Exercise,ExerciseConfig)
admin.site.register(Group1,Group1Config)
