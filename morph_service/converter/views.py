'''The definition of each view'''
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import tempfile
from io import open  # pylint: disable=redefined-builtin

from django.core.files.storage import FileSystemStorage
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from morph_tool import converter
# pylint: disable=import-error
from requests.utils import unquote

L = logging.getLogger()


def index(_):
    '''Returns the template index.html'''
    return render_to_response('index.html')


class MyJsonResponse(JsonResponse):
    '''JSon response that handles binary data'''
    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        json_dumps_params = dict(ensure_ascii=False)
        super(MyJsonResponse, self).__init__(data, encoder, safe, json_dumps_params, **kwargs)


def api(request):
    '''Return a NeuroLucida file with the NeuroM annotations appended at then end'''
    if request.method == 'OPTIONS':
        return HttpResponse(204)

    if request.method == 'POST' and request.FILES:
        try:
            a_file = next(iter(request.FILES.values()))
            tmp = tempfile.gettempdir()
            file_system_storage = FileSystemStorage(tmp)
            filename = file_system_storage.save(a_file.name, a_file)

            uploaded_file_url = os.path.join(
                tmp, unquote(file_system_storage.url(filename)))
            filename_no_ext = a_file.name.split('.')[0]
            output_extension = request.POST.get('output_extension')
            output_filename = os.path.join('/tmp',
                                           filename_no_ext + output_extension)
            converter.run(uploaded_file_url, output_filename)
        except Exception as exception:  # pylint: disable=broad-except
            L.error(str(exception))
            return JsonResponse({'error': 'Error while loading the neuron.\n{}'.format(
                exception)}, status=400)

        filename = filename_no_ext + output_extension
        if output_extension == '.h5':
            flag = 'rb'
            content_type = 'application/octet-stream'
        else:
            flag = 'r'
            content_type = 'text/plain'

        with open(output_filename, flag) as filep:
            data = filep.read()
            response = HttpResponse(content_type=content_type)
            # response['Content-Disposition'] = 'attachment; filename=%s' % filename
            response.write(data)
            return response

    return HttpResponse(200)
