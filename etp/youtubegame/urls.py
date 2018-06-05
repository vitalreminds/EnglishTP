from django.urls import path
from .views import redirectview, YoutubeVideoTryView, endGame, YoutubeVideoCreate,  YoutubeVideoPlayView, YoutubeVideoDelete, YoutubeVideoDetailView, YoutubeVideoUpdate, YoutubeVideoListView


# Urls

youtubegame_patterns = ([ 
    path('videos', YoutubeVideoListView.as_view(), name='videos'),
    path('try/', YoutubeVideoTryView.as_view(), name='try'),    
    path('', redirectview , name='index'),
    path('play/P<pk>/', YoutubeVideoPlayView.as_view(), name='play'),    
    path('create/', YoutubeVideoCreate.as_view(), name='create'),
    path('update/P<pk>/', YoutubeVideoUpdate.as_view(), name='update'),
    path('delete/P<pk>/', YoutubeVideoDelete.as_view(), name='delete'),
    path('endgame/', endGame, name='endgame'),        
       
],'youtubegame')