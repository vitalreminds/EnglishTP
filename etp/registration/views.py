from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django import forms
from .models import Profile, Teacher, Alumn
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

# Decorador propio para las vistas 

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(user):
        if user.is_authenticated:
            if bool(user.groups.filter(name__in=group_names)) | user.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

def notlogin_required():
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(user):
        if user.is_authenticated:
            return False
        return True
    return user_passes_test(in_groups)

def is_admin():
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(user):
        if user.is_superuser or not user.is_authenticated:
            return True
        return False
    return user_passes_test(in_groups)

def is_admin1():
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(user):
        if user.is_superuser:
            return True
        return False
    return user_passes_test(in_groups)


# Create your views here.
@method_decorator(is_admin(),name='dispatch')
class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        my_group = Group.objects.get(name='Alumno')
        if self.request.user.is_superuser:
            return reverse_lazy('signup')+'?okregister'
        else:
            return reverse_lazy('login')+'?register'
            

    def get_form(self, form_class=None):
        form = super(SignUpView,self).get_form()
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control mb-2','placeholder':'Nombre de usario'})
        form.fields['username'].help_text = ""        
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2','placeholder':'Email'})        
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2','placeholder':'Contraseña'})
        form.fields['password1'].help_text = ""                
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2','placeholder':'Confirmar contraseña'})
        form.fields['password2'].help_text = ""                        
        if not self.request.user.is_superuser:
            form.fields['kind'].widget = forms.HiddenInput()
        return form

class ProfileDetail(ListView):
    model=Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context


class ProfileUpdateById(UpdateView):
    form_class = ProfileForm
    model = Profile
    template_name = 'registration/profile_form.html'
    def get_success_url(self):
        return reverse_lazy('update_profilebyid',args=[self.object.id])+'?okupdate'

class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    model = Profile
    template_name = 'registration/profile_form.html'

    def get_object(self):
        profile = Profile.objects.get(user=self.request.user)
        return profile

    def get_success_url(self):
        return reverse_lazy('update_profile')+'?okupdate'

    def get_form(self, form_class=None):
        form = super(ProfileUpdate,self).get_form()
        form.fields['avatar'].help_text = ""        
        return form

class DeleteUserListView(ListView):
    model = User
    template_name = 'registration/user_list.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(DeleteUserListView, self).get_context_data(*args, **kwargs)
        alumns = Alumn.objects.all()
        teachers = Teacher.objects.all()
        providers = User.objects.filter(groups__name='Proveedor')
        
        x = []
        for alumn in alumns:
            x.append(Profile.objects.get(user=alumn.user))

        ctx['Alumns'] = x

        x = []
        for teacher in teachers:
            x.append(Profile.objects.get(user=teacher.user))

        ctx['Teachers'] = x

        x = []
        for provider in providers:
            x.append(Profile.objects.get(user=provider))

        ctx['Providers'] = x
        
        return ctx
        
    
def delete_user(request, username):
    try:
        u = User.objects.get(username = username)
        alumn = Alumn.objects.filter(user=u).first()
        teacher = Teacher.objects.filter(user=u).first()

        if alumn:
            alumn.delete()
        if teacher:
            teacher.delete()
        u.delete()  
        return redirect(reverse('delete_userlist')+'?okdelete')    

    except User.DoesNotExist:  
        return redirect(reverse('delete_userlist')+'?notdelete')    
        
        
class EmailUpdate(UpdateView):
    form_class = EmailForm
    template_name = 'registration/profile_email_form.html'

    def get_success_url(self):
        return reverse_lazy('profile')+'?okemail'

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate,self).get_form()
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2','placeholder':'Email'})

        return form