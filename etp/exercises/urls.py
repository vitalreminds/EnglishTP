from django.urls import path, include
from .views import ExerciseListView ,ExerciseCreate, ExerciseUpdate, ExerciseDelete, download_exercise, GroupListView, GroupCreateView, GroupDeleteView, GroupUpdateView


# Urls

Exercise_patterns = ([ 
    path('exercises/<slug:slug>/', ExerciseListView.as_view(), name='exercises'),
    path('create/<slug:slug>/', ExerciseCreate.as_view(), name='create'),
    path('update/P<pk>/', ExerciseUpdate.as_view(), name='update'),
    path('delete/<slug:slug>/<int:pk>/', ExerciseDelete.as_view(), name='delete'),
    path('download/P<id>/', download_exercise, name='download'),  
    #Grupos
    path('', GroupListView.as_view(), name='groups'),
    path('group/create/', GroupCreateView.as_view(), name='creategroup'),
    path('group/delete/P<pk>/', GroupDeleteView.as_view(), name='deletegroup'),
    path('group/update/P<pk>/', GroupUpdateView.as_view(), name='updategroup')  
      
        
              
],'exercises')