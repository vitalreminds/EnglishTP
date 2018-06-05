from django.urls import path, include
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-me/', views.about, name='about'),
    path('game/', views.game, name='game'),
]