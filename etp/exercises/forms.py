from django import forms
from .models import Exercise
from django.contrib.auth.models import User
from registration.models import Teacher, Alumn
from exercises.models import Group1
from django.forms.widgets import ClearableFileInput

class MyClearableFileInput(ClearableFileInput):
    initial = ''
    input_text = 'Cambiar'
    clear_checkbox_label = 'Borrar?'

global user
global name

class DateInput(forms.DateInput):
    input_type = 'date'

class ExerciseForm(forms.ModelForm):
    
    class Meta:
        model = Exercise
        fields = ['title','url','date_delivery']
        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'Titulo'}) ,
            'url':  MyClearableFileInput (attrs={'class':'form-control mt-1'}),            
            'date_delivery': DateInput(attrs={'class' : 'form-control', 'placeholder':'Fecha de entrega'})            
            }
    
    def __init__(self, *args, **kwargs):
        global user, name
        if 'place_user' in kwargs:
            user = kwargs.pop('place_user')
        if 'place_name' in kwargs:
            name = kwargs.pop('place_name')
        # now kwargs doesn't contain 'place_user', so we can safely pass it to the base class method
        super(ExerciseForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        global user, name
        
        exercise = super().save(commit=False)
        if  not exercise.teacher:
            teach = Teacher.objects.get(user=user)
            group = Group1.objects.get(name=name.upper())
            exercise.teacher = teach 
            exercise.group = group          
        if commit:
            exercise.save()
        return exercise


class Group1Form(forms.ModelForm):

    alumn = forms.ModelMultipleChoiceField(required=False,queryset= Alumn.objects.all(), widget=forms.SelectMultiple(attrs={'class' : 'form-control'}) ) 
    teacher = forms.ModelChoiceField(queryset= Teacher.objects.all(), widget=forms.Select(attrs={'class' : 'form-control'}))           
    class Meta:
        model = Group1

        fields = ['name', 'alumn','teacher']
        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'Nombre del grupo'}) ,
            }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        name = name.upper()

        return name
        