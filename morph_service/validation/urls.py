'''The routing of the validation app urls'''
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^/api$', views.api, name='api'),
]
