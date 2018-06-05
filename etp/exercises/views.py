from django.shortcuts import render, HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from .models import Exercise, Group1
from .forms import ExerciseForm, Group1Form
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.http import FileResponse
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Decorador propio para las vistas 

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(user):
        if user.is_authenticated:
            if bool(user.groups.filter(name__in=group_names)) | user.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)


# Create your views here.


class ExerciseListView(ListView):
    model = Exercise

    def get_context_data(self, *args, **kwargs):
        ctx = super(ExerciseListView, self).get_context_data(*args, **kwargs)
        ctx['slug'] = self.kwargs['slug'] # or Tag.objects.get(slug=...)
        return ctx


@method_decorator(group_required('Profesor'),name='dispatch')
class ExerciseCreate(CreateView):
    model = Exercise
    form_class = ExerciseForm

    def get_success_url(self):
        return reverse_lazy('exercises:exercises', kwargs={'slug':self.kwargs['slug']})+'?okcreate'

    def get_context_data(self, *args, **kwargs):
        ctx = super(ExerciseCreate, self).get_context_data(*args, **kwargs)
        ctx['slug'] = self.kwargs['slug'] # or Tag.objects.get(slug=...)
        return ctx

    def get_form_kwargs(self):
        kwargs = super(ExerciseCreate, self).get_form_kwargs()
        kwargs.update({'place_user': self.request.user, 'place_name': self.kwargs['slug']})
        return kwargs
    

@method_decorator(group_required('Profesor'),name='dispatch')
class ExerciseUpdate(UpdateView):
    model = Exercise
    form_class = ExerciseForm
       
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('exercises:update', args=[self.object.id])+'?okupdate'


@method_decorator(group_required('Profesor'),name='dispatch')
class ExerciseDelete(DeleteView):
    model = Exercise

    def get_success_url(self):
        return reverse_lazy('exercises:exercises', kwargs={'slug':self.kwargs['slug']})+'?okdelete'


class GroupListView(ListView):
    model = Group1
    paginate_by = 4

class GroupCreateView(CreateView):
    model=Group1
    form_class = Group1Form

    def get_success_url(self):
        return reverse_lazy('exercises:groups')+'?okcreate'

class GroupDeleteView(DeleteView):
    model = Group1

    def get_success_url(self):
        return reverse_lazy('exercises:groups')+'?okdelete'


class GroupUpdateView(UpdateView):
    model = Group1
    form_class = Group1Form
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('exercises:updategroup', args=[self.object.id])+'?okupdate'


def download_exercise(request, id):
    exercise = Exercise.objects.get(id=id)
    url = exercise.url.url
    ext = url.split('.')[1] 
    path1 = BASE_DIR+url
    fsock = open(path1, 'rb')
    response = HttpResponse(fsock, content_type='aplication/pdf')
    response['Content-Disposition'] = "attachment; filename=%s.%s" % (exercise.title,ext)
    return response