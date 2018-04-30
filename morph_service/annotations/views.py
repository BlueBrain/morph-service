'''The definition of each view'''
import os
import tempfile
import urllib
from functools import partial

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render

import neurom
from neurom.apps.annotate import annotate
from neurom.check.neuron_checks import (has_no_dangling_branch,
                                        has_no_fat_ends, has_no_jumps,
                                        has_no_narrow_start)

from morph_service.version import VERSION


CHECKERS = {has_no_fat_ends: {"name": "fat end",
                              "label": "Circle3",
                              "color": "Blue"},
            partial(has_no_jumps, axis='z'): {"name": "zjump",
                                              "label": "Circle2",
                                              "color": "Green"},
            has_no_narrow_start: {"name": "narrow start",
                                  "label": "Circle1",
                                  "color": "Blue"},
            has_no_dangling_branch: {"name": "dangling",
                                     "label": "Circle6",
                                     "color": "Magenta"}}


def index(request):
    '''Returns the template index.html'''
    return render(request, 'annotations/index.html', {'version': VERSION})


def api(request):
    '''Return a NeuroLucida file with the NeuroM annotations appended at then end'''
    if request.method == 'POST' and request.FILES:
        try:
            a_file = next(iter(request.FILES.values()))
            tmp = tempfile.gettempdir()
            file_system_storage = FileSystemStorage(tmp)
            filename = file_system_storage.save(a_file.name, a_file)

            if a_file.name.split('.')[-1].lower() != 'asc':
                raise UnrecognizedMorphologyFormat()

            uploaded_file_url = os.path.join(
                tmp, urllib.parse.unquote(file_system_storage.url(filename)))

            neuron = neurom.load_neuron(uploaded_file_url)
        except UnrecognizedMorphologyFormat:
            return JsonResponse({'error': '\n'.join(['Only the NeuroLucida format is supported',
                                                     'The file must have the "asc" extension'])},
                                status=400)
        except Exception as exception:  # pylint: disable=broad-except
            return JsonResponse({'error': 'Error while loading the neuron.\n{}'.format(
                exception)}, status=400)

        results = [checker(neuron) for checker in CHECKERS]
        annotations = annotate(results, CHECKERS.values())

        if annotations:
            with open(uploaded_file_url, 'a') as outf:
                outf.write(annotations)

        with open(uploaded_file_url, encoding='utf-8', errors='replace') as outf:
            return JsonResponse({'summary': {setting['name']: len(result.info)
                                             for result, setting in zip(results, CHECKERS.values())
                                             if result.info},
                                 'file': ''.join(outf.readlines())})
        return JsonResponse({'status': 'ok'})


class UnrecognizedMorphologyFormat(Exception):
    '''An exception when morph file is not in ASC format'''
