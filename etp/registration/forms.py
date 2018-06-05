from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from registration.models import Alumn, Profile, Teacher
from django.forms.widgets import ClearableFileInput

class MyClearableFileInput(ClearableFileInput):
    initial = ''
    input_text = 'Cambiar'
    clear_checkbox_label = 'Borrar?'
    
class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True)

    options = (
        ('a','Alumno'),
        ('b','Profesor'),
        ('c','Proveedor'),
    )
    kind = forms.ChoiceField(choices=options, required=True, initial='a', widget = forms.Select(attrs={'class':'form-control mb-2'}))
    name = forms.CharField(required=True, max_length=15 ,widget = forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Nombre'}))
    latsname1 = forms.CharField(required=True, max_length=15 ,widget = forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Primer apellido'}))
    latsname2 = forms.CharField(required=True, max_length=15 ,widget = forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Segundo apellido'}))
    key = forms.CharField(required=True, max_length=10 ,widget = forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Boleta, Numero de empleado'}))
    phone = forms.CharField(required=True, max_length=10 ,widget = forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Telefono'}))
    

    class Meta:
        model = User
        fields = ('username','name', 'latsname1', 'latsname2', 'phone' ,'key', 'email','password1','password2','kind')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        alumn = User.objects.filter(email=email)
        if alumn.exists():
            raise forms.ValidationError('Ya existe una cuenta con el mismo email, Prueba con otro') 
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        alumn = User.objects.filter(username=username)
        if alumn.exists():
            raise forms.ValidationError('Ya existe una cuenta con el mismo usuario, Prueba con otro') 
        return username

    def save(self, commit=True):
        kind = self.cleaned_data.get('kind')
        name = self.cleaned_data.get('name')
        lastname1 = self.cleaned_data.get('latsname1')
        lastname2 = self.cleaned_data.get('latsname2')
        key = self.cleaned_data.get('key')
        phone = self.cleaned_data.get('phone')
        
                                
        user = super().save(commit=False) 
        if commit:
            user.save()

            if kind == 'a' :
                my_group = Group.objects.get(name='Alumno')
                Alumn.objects.get_or_create(user=user)  
                p,created = Profile.objects.get_or_create(user=user)
                p.name = name
                p.lastname1 = lastname1
                p.lastname2 = lastname2
                p.key = key
                p.phone = phone
                p.save()
                my_group.user_set.add(user) 

            if kind == 'b' :
                my_group = Group.objects.get(name='Profesor')   
                Teacher.objects.get_or_create(user=user)
                p,created = Profile.objects.get_or_create(user=user)
                p.name = name
                p.lastname1 = lastname1
                p.phone = phone
                p.lastname2 = lastname2
                p.key = key
                p.save()               
                my_group.user_set.add(user) 

            if kind == 'c' :
                p,created = Profile.objects.get_or_create(user=user)
                p.name = name
                p.phone = phone
                p.lastname1 = lastname1
                p.lastname2 = lastname2
                p.key = key
                p.save()                                
                my_group = Group.objects.get(name='Proveedor')   
                my_group.user_set.add(user) 

        return user  

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'name', 'lastname1', 'lastname2', 'phone']
        widgets = {
            'avatar':  MyClearableFileInput (attrs={'class':'form-control-file mt-3'}),
            'name': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Nombre'}),
            'lastname1': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Apellido Paterno'}),
            'lastname2': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Apellido Paterno'}),                       
            'phone': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Telefono'}),
            'key': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Clave'}),
            'score': forms.NumberInput(attrs={'class':'form-control mt-3', 'placeholder':'Score'})
        }



class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        alumn = User.objects.filter(email=email)
        if 'email' in self.changed_data:
            if alumn.exists():
                raise forms.ValidationError('Ya existe una cuenta con el mismo email, Prueba con otro') 
        return email