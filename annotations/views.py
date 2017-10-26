import os
import tempfile

import neurom
from neurom.apps.annotate import annotate

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'annotations/index.html')


def api(request):
    if request.method == 'POST' and request.FILES:
        f = next(request.FILES.values())
        tmp = tempfile.gettempdir()
        fs = FileSystemStorage(tmp)
        basename = f.name.split('.')[0]
        filename = fs.save(f.name, f)

        if f.name.split('.')[-1].lower() != 'asc':
            return HttpResponse('\n'.join(['<h1>Only the NeuroLucida format is supported</h1>'
                                           '<h2>The file must have the "asc" extension']),
                                status=400)

        uploaded_file_url = os.path.join(tmp, fs.url(filename))
        try:
            neuron = neurom.load_neuron(uploaded_file_url)
        except Exception as e:
            return HttpResponse('Error while loading the neuron.\n{}'.format(e))
        annotations = annotate(neuron)
        if annotations:
            with open(uploaded_file_url, 'a') as f:
                f.write(annotations)

        with open(uploaded_file_url) as f:
            response = HttpResponse(f, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="{}-annotated.asc"'.format(
                basename)
            return response
