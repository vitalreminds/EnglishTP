from django.contrib import admin
from .models import Alumn, Teacher

# Register your models here.
class TeacherConfig(admin.ModelAdmin):
    pass

class AlumnConfig(admin.ModelAdmin):
    pass

admin.site.register(Teacher,TeacherConfig)
admin.site.register(Alumn,AlumnConfig)
