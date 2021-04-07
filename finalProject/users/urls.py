from typing import Pattern
from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    # ^ : start with , $ : end with nothing ( /posts/nothing ) only /posts
    url(r'^$', views.index, name='index'),
    #?P : parameter , (parameter is id) , \d : it should be a digit , + it should be at least 1 or more digits
    url(r'^details/(?P<id>\d+)/$', views.details, name='details'),
    url(r'^registerUser/$', views.registerUser, name='register'),
    url(r'^editUser/(?P<id>\d+)$', views.editUser, name='edit'),
    url(r'^deleteUser/(?P<id>\d+)$', views.deleteUser, name='delete'),
    url(r'^about/$', views.about, name='about'),
];