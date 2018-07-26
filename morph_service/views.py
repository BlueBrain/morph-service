'''MorphService housekeeping views'''
from django.http import HttpResponse
from django.shortcuts import render_to_response


def status(_):
    '''Used as a polled point to check that the website is up and running'''
    return HttpResponse('morph_service_status 1', status='200')


def index(_):
    '''index'''
    return render_to_response('index.html')
