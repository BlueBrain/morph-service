'''The definition of each view'''
import logging
import os
import tempfile

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render_to_response
from future.standard_library import install_aliases
from requests.utils import unquote

from morphio import MorphioError  # pylint: disable=no-name-in-module
from neurom import load_neuron

from morph_service.validation.validator import validation_report
install_aliases()
L = logging.getLogger()


def index(_):
    '''Returns the template index.html'''
    return render_to_response('index.html')


def get_neuron_file(request):
    '''Returns the path to the neuron'''
    a_file = next(iter(request.FILES.values()))
    tmp = tempfile.gettempdir()
    file_system_storage = FileSystemStorage(tmp)
    filename = file_system_storage.save(a_file.name, a_file)

    if a_file.name.split('.')[-1].lower() not in {'asc', 'h5', 'swc'}:
        raise UnrecognizedMorphologyFormat()

    uploaded_file_url = os.path.join(
        tmp, unquote(file_system_storage.url(filename)))

    return uploaded_file_url


# pylint: disable=too-many-return-statements
def api(request):
    '''Return a NeuroLucida file with the NeuroM annotations appended at then end'''
    if request.method == 'OPTIONS':
        return HttpResponse(204)

    if request.method == 'POST' and request.FILES:
        try:
            filename = get_neuron_file(request)
        except Exception as exception:  # pylint: disable=broad-except
            L.error(str(exception))
            return JsonResponse({'error': 'Error while fetching the neuron file from '
                                          'the payload.\n{}'.format(exception)}, status=400)

        try:
            neuron = load_neuron(filename)
        except MorphioError as exception:
            return JsonResponse({'error': 'Error while opening the neuron with MorphIO:\n{}'.format(
                exception)}, status=400)

        if not neuron.neurites:
            return JsonResponse({'error': 'Error: {} has no neurites'.format(
                os.path.basename(filename))}, status=400)

        if neuron.soma.points.size == 0:
            return JsonResponse({'error': 'Error: {} has no soma'.format(
                os.path.basename(filename))}, status=400)

        return JsonResponse(validation_report(neuron))
    return HttpResponse(200)


class UnrecognizedMorphologyFormat(Exception):
    '''An exception when the morph file is not in ASC format'''
