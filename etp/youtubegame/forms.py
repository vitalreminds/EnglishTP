from django import forms
from .models import YoutubeVideo
from django.contrib.auth.models import User
import pafy
pafy.BACK_END = "internal"

from django.forms.widgets import ClearableFileInput

class MyClearableFileInput(ClearableFileInput):
    initial = ''
    input_text = 'Cambiar'
    clear_checkbox_label = 'Borrar?'


class YoutubeVideoForm(forms.ModelForm):
    
    class Meta:
        model = YoutubeVideo
        fields = ['videoId','letter','words']
        widgets = {
            'videoId' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'VideoId'}) ,            
            'letter':  MyClearableFileInput (attrs={'class':'form-control mt-1'}),
            'words':  MyClearableFileInput (attrs={'class':'form-control mt-1'})               
            
        }

    def save(self, commit=True):
        youtubevideo = super().save(commit=False)
        if  not youtubevideo.title:
            url = "https://www.youtube.com/watch?v="+youtubevideo.videoId
            video = pafy.new(url)  
            youtubevideo.title =  video.title
            youtubevideo.views =  video.viewcount  
            youtubevideo.duration =  video.duration   
               
        if commit:
            youtubevideo.save()
        return youtubevideo