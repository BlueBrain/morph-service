'''The routing of the annotation app urls'''
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^summary$', views.summary, name='summary'),
    url(r'^api$', views.api, name='api'),
]
