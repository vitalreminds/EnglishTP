from django import forms
from .models import Book
from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput

class MyClearableFileInput(ClearableFileInput):
    initial = ''
    input_text = 'Cambiar'
    clear_checkbox_label = 'Borrar?'
global user

class BookForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = ['title', 'description','autor','edition','editorial','cover_page','price','ISBN']
        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'Titulo'}) ,
            'description': forms.Textarea(attrs={'class' : 'form-control', 'placeholder':'Descripcion'}) ,
            'autor': forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'Autor'}) ,
            'edition': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'Edicion'}) , 
            'editorial': forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'Editorial'}) ,
            'cover_page':  MyClearableFileInput (attrs={'class':'form-control mt-1'}),
            'price' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'Precio'}),
            'ISBN' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'ISBN'})
            
        }

    def __init__(self, *args, **kwargs):
        global user
        if 'place_user' in kwargs:
            user = kwargs.pop('place_user')
        # now kwargs doesn't contain 'place_user', so we can safely pass it to the base class method
        super(BookForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        global user
        book = super().save(commit=False)
        if  not book.provider:
            book.provider = user      
        if commit:
            book.save()
        return book
        