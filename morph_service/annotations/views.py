'''The definition of each view'''
import urllib
import os
import tempfile

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

import neurom
from neurom.apps.annotate import annotate


def index(request):
    '''Returns the template index.html'''
    return render(request, 'annotations/index.html')


def api(request):
    '''Return a NeuroLucida file with the NeuroM annotations appended at then end'''
    if request.method == 'POST' and request.FILES:
        a_file = next(iter(request.FILES.values()))
        tmp = tempfile.gettempdir()
        fs = FileSystemStorage(tmp)
        basename = a_file.name.split('.')[0]
        filename = fs.save(a_file.name, a_file)

        if a_file.name.split('.')[-1].lower() != 'asc':
            return HttpResponse('\n'.join(['<h1>Only the NeuroLucida format is supported</h1>'
                                           '<h2>The file must have the "asc" extension']),
                                status=400)

        uploaded_file_url = os.path.join(tmp, urllib.parse.unquote(fs.url(filename)))
        try:
            neuron = neurom.load_neuron(uploaded_file_url)
        except Exception as e:  # pylint: disable=broad-except
            return HttpResponse('Error while loading the neuron.\n{}'.format(e))
        annotations = annotate(neuron)
        if annotations:
            with open(uploaded_file_url, 'a') as f:
                f.write(annotations)

        with open(uploaded_file_url, encoding='utf-8', errors='replace') as f:
            response = HttpResponse(f, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="{}-annotated.asc"'.format(
                basename)
            return response
