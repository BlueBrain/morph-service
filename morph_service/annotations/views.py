'''The definition of each view'''
import os
import tempfile
import urllib
from functools import partial

import neurom
from neurom.apps.annotate import annotate
from neurom.check.neuron_checks import (has_no_dangling_branch,
                                        has_no_fat_ends, has_no_jumps,
                                        has_no_narrow_start)

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

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
    return render(request, 'annotations/index.html')


def api(request):
    '''Return a NeuroLucida file with the NeuroM annotations appended at then end'''
    if request.method == 'POST' and request.FILES:
        try:
            a_file = next(iter(request.FILES.values()))
            tmp = tempfile.gettempdir()
            fs = FileSystemStorage(tmp)
            basename = a_file.name.split('.')[0]
            filename = fs.save(a_file.name, a_file)

            if a_file.name.split('.')[-1].lower() != 'asc':
                raise UnrecognizedMorphologyFormat()

            uploaded_file_url = os.path.join(tmp, urllib.parse.unquote(fs.url(filename)))

            neuron = neurom.load_neuron(uploaded_file_url)
        except UnrecognizedMorphologyFormat:
            return HttpResponse('\n'.join(['<h1>Only the NeuroLucida format is supported</h1>'
                                           '<h2>The file must have the "asc" extension']),
                                status=400)
        except Exception as e:  # pylint: disable=broad-except
            return HttpResponse('Error while loading the neuron.\n{}'.format(e))

        results = [checker(neuron) for checker in CHECKERS]
        annotations = annotate(results, CHECKERS.values())

        if annotations:
            with open(uploaded_file_url, 'a') as f:
                f.write(annotations)

        with open(uploaded_file_url, encoding='utf-8', errors='replace') as f:
            response = HttpResponse(f, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="{}-annotated.asc"'.format(
                basename)
            return response


class UnrecognizedMorphologyFormat(Exception):
    '''An exception when morph file is not in ASC format'''


def summary(request):
    '''Return a NeuroLucida file with the NeuroM annotations appended at then end'''
    if request.method == 'POST' and request.FILES:
        try:
            a_file = next(iter(request.FILES.values()))
            tmp = tempfile.gettempdir()
            fs = FileSystemStorage(tmp)
            filename = fs.save(a_file.name, a_file)

            if a_file.name.split('.')[-1].lower() != 'asc':
                raise UnrecognizedMorphologyFormat()

            f = os.path.join(tmp, urllib.parse.unquote(fs.url(filename)))

            neuron = neurom.load_neuron(f)
        except UnrecognizedMorphologyFormat:
            return HttpResponse('\n'.join(['<h1>Only the NeuroLucida format is supported</h1>'
                                           '<h2>The file must have the "asc" extension']),
                                status=400)
        except Exception as e:  # pylint: disable=broad-except
            return HttpResponse('Error while loading the neuron.\n{}'.format(e))

        results = [checker(neuron) for checker in CHECKERS]
        _summary = {setting['name']: len(result.info)
                    for result, setting in zip(results, CHECKERS.values())
                    if result.info}
        html_list = ''.join("<li>{}: {}</li>".format(name, res) for name, res in _summary.items())
        ret = "<h3>Annotation summary</h3><ul>{}</ul>".format(html_list)
        return HttpResponse(ret)
