from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/', views.about, name='about'),
    url(r'^music/', views.music, name='music'),
    url(r'^github/', views.github, name='github'),
    url(r'^api/music/', views.api_music, name='api')
]

