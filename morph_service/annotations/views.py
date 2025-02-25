'''The definition of each view'''
import logging
import os
import tempfile
from functools import partial
from io import open  # pylint: disable=redefined-builtin
from future.standard_library import install_aliases
from requests.utils import unquote

import neurom
from neurom.apps.annotate import annotate
from neurom.check.neuron_checks import (has_no_dangling_branch,
                                        has_no_fat_ends, has_no_jumps,
                                        has_no_narrow_start,
                                        has_no_single_children,
                                        has_multifurcation)

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render_to_response


install_aliases()
L = logging.getLogger()

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
                                     "color": "Magenta"},

            has_no_single_children: {"name": "single children",
                                     "label": "Circle7",
                                     "color": "Red"},

            has_multifurcation: {"name": "Multifurcation",
                                 "label": "Circle8",
                                 "color": "Yellow"}}


def index(_):
    '''Returns the template index.html'''
    return render_to_response('index.html')


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

            if a_file.name.split('.')[-1].lower() != 'asc':
                raise UnrecognizedMorphologyFormat()

            uploaded_file_url = os.path.join(
                tmp, unquote(file_system_storage.url(filename)))

            neuron = neurom.load_neuron(uploaded_file_url)
        except UnrecognizedMorphologyFormat:
            return JsonResponse({'error': '\n'.join(['Only the NeuroLucida format is supported',
                                                     'The file must have the "asc" extension'])},
                                status=400)
        except Exception as exception:  # pylint: disable=broad-except
            L.error(str(exception))
            return JsonResponse({'error': f'Error while loading the neuron.\n{exception}'},
                                status=400)

        results = [checker(neuron) for checker in CHECKERS]
        annotations = annotate(results, CHECKERS.values())

        if annotations:
            with open(uploaded_file_url, 'a', encoding='utf-8') as outf:
                outf.write(annotations)

        with open(uploaded_file_url, encoding='utf-8', errors='replace') as outf:
            return JsonResponse({'summary': {setting['name']: len(result.info)
                                             for result, setting in zip(results, CHECKERS.values())
                                             if result.info},
                                 'file': ''.join(outf.readlines())})
        return JsonResponse({'status': 'ok'})
    return HttpResponse(200)


class UnrecognizedMorphologyFormat(Exception):
    '''An exception when the morph file is not in ASC format'''
