from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dash, name='dash'),
    path('helpline/', views.help, name='help'),
    path('news/', views.news, name='news'),
]

