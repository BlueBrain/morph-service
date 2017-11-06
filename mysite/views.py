from django.http import HttpResponse


def status(request):
    return HttpResponse('morph_service_status 1', status='200')
