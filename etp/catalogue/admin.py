from django.contrib import admin
from .models import Book

# Register your models here.
class BookConfig(admin.ModelAdmin):
    readonly_fields = ('created','updated')

    class Media:
        css = {
            'all': ('catalogue/css/custom_ckeditor1.css',)
        }

admin.site.register(Book,BookConfig)