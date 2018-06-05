from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect, render_to_response
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse
from .models import YoutubeVideo
from .forms import YoutubeVideoForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from registration.models import Profile
import pafy
from django.views.generic.base import TemplateView

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


def redirectview(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('youtubegame:videos'))
    else:
        return HttpResponseRedirect(reverse_lazy('youtubegame:try'))
    
class YoutubeVideoTryView(TemplateView):

    template_name = "youtubegame_try.html"

class YoutubeVideoDetailView(DetailView):
    model = YoutubeVideo
    
class YoutubeVideoListView(ListView):
    model = YoutubeVideo
    paginate_by = 4

class YoutubeVideoCreate(CreateView):
    model = YoutubeVideo
    form_class = YoutubeVideoForm
    
    def get_success_url(self):
        return reverse_lazy('youtubegame:videos')+'?okcreate'

class YoutubeVideoPlayView(DetailView):
    model = YoutubeVideo
    

class YoutubeVideoUpdate(UpdateView):
    model = YoutubeVideo
    form_class = YoutubeVideoForm
       
    template_name_suffix = '_update_form'

    def get_success_url(self):
        x = self.kwargs
        return reverse_lazy('youtubegame:update',kwargs={'pk': x['pk']})+'?okupdate'


class YoutubeVideoDelete(DeleteView):
    model = YoutubeVideo
    def get_success_url(self):
        return reverse_lazy('youtubegame:videos')+'?okdelete'

def endGame(request):
    profile = Profile.objects.get(user=request.user)
    x = int(request.POST.get("score", ""))
    profile.score += x
    profile.save()

    return HttpResponseRedirect(reverse('youtubegame:videos'))