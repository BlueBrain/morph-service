'''Morphology classifier application'''

from __future__ import unicode_literals

import json
import os
import tempfile
import pkg_resources

import numpy as np
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response

import tmd

from tmd.Topology.analysis import get_limits, get_persistence_image_data


def index(_):
    '''Returns the template index.html'''
    return render_to_response('index.html')


LIST_OF_MODULES = ['discriminant_analysis', 'discriminant_analysis', 'tree']

LIST_OF_CLASSIFIERS = ['LinearDiscriminantAnalysis',
                       'QuadraticDiscriminantAnalysis', 'DecisionTreeClassifier']


def train(mod, classifier, data, labels, **kwargs):
    '''Trains the classifier from mod of sklearn
       with data and targets.
       Returns a fited classifier.
    '''
    import importlib

    clas_mod = importlib.import_module('sklearn.' + mod)
    clf = getattr(clas_mod, classifier)()
    clf.set_params(**kwargs)

    clf.fit(data, labels)

    return clf


def predict(clf, data):
    '''Predict label for data for the trained classifier clf.
       Returns the index of the predicted class
       for each datapoint in data.
    '''
    predict_label = clf.predict([data])

    return predict_label[0]


def trainer(groups, neurite_type):
    '''Return train dataset'''
    # Generate a persistence diagram per neuron
    pers_diagrams = [tmd.methods.get_ph_neuron(j, neurite_type=neurite_type)
                     for group in groups for j in group.neurons]

    xlims, ylims = get_limits(pers_diagrams)
    # Generate a persistence image for each diagram
    pers_images = [get_persistence_image_data(p, xlims=xlims, ylims=ylims)
                   for p in pers_diagrams]
    # Create the train dataset from the flatten images
    train_dataset = [img.flatten() for img in pers_images]
    return train_dataset, xlims, ylims


def tester(cell_to_classify, neurite_type, xlims, ylims):
    '''Return test dataset'''
    # ------------------------ Test cell dataset -------------------------------
    # Load cell to be classified
    neuron2test = tmd.io.load_neuron(cell_to_classify)
    # Get persistence diagram from test cell
    pers2test = tmd.methods.get_ph_neuron(neuron2test, neurite_type=neurite_type)
    # Get persistence image from test cell
    pers_image2test = get_persistence_image_data(pers2test, xlims=xlims, ylims=ylims)
    # Create the test dataset from the flatten image of the test cell
    return pers_image2test.flatten()


def train_and_test(groups, neurite_type, cell_to_classify):
    '''Return training and testing dataset'''
    train_dataset, xlims, ylims = trainer(groups, neurite_type)
    test_dataset = tester(cell_to_classify, neurite_type, xlims, ylims)
    return train_dataset, test_dataset


def percentages(groups, predict_labels, labels):
    '''Percentages'''
    return {groups[i - 1].name:
            np.float(len(np.where(np.array(predict_labels) == i)[0])) / len(predict_labels)
            for i in np.unique(labels)}


def generate_groups(list_of_groups):
    '''Morpholog groups'''
    base = pkg_resources.resource_filename('morph_service', 'classifier/training_sample')
    return [tmd.io.load_population(os.path.join(base, l))
            for l in list_of_groups]


# pylint: disable=too-many-arguments
def classify_cell_in_groups(list_of_groups,
                            cell_to_classify,
                            neurite_type='apical',
                            classifier_module=LIST_OF_MODULES[0],
                            classifier_method=LIST_OF_CLASSIFIERS[0],
                            number_of_trials=20):
    '''The classifier'''
    groups = generate_groups(list_of_groups)
    # Define labels depending on the number of neurons in each folder
    labels = [i + 1 for i, k in enumerate(groups) for _ in k.neurons]

    train_dataset, test_dataset = train_and_test(groups, neurite_type, cell_to_classify)

    # Train classifier with training images for selected number_of_trials
    predict_labels = [
        predict(train(classifier_module, classifier_method, train_dataset, labels),
                test_dataset)
        for _ in range(number_of_trials)]

    # Test classifier with test image and return predictions
    return percentages(groups, predict_labels, labels)


def api(request):
    '''Return a NeuroLucida file with the NeuroM annotations appended at then end'''
    if request.method == 'OPTIONS':
        return HttpResponse(204)

    if request.method == 'POST' and request.FILES:
        a_file = next(iter(request.FILES.values()))
        tmp = tempfile.gettempdir()
        file_system_storage = FileSystemStorage(tmp)
        filename = file_system_storage.save(a_file.name, a_file)

        amount_trials = int(request.POST['trials']) or 1
        morphology_types = json.loads(request.POST['morphtypes']) or [
            'L5_UPC', 'L5_TPC_A', 'L5_TPC_B', 'L5_TPC_C']
        selected_classifier = request.POST['classifier'] or 'LinearDiscriminantAnalysis'
        classifier_index = LIST_OF_CLASSIFIERS.index(selected_classifier)
        result = classify_cell_in_groups(list_of_groups=morphology_types,
                                         cell_to_classify=os.path.join(tmp, filename),
                                         neurite_type='apical',
                                         classifier_module=LIST_OF_MODULES[classifier_index],
                                         classifier_method=LIST_OF_CLASSIFIERS[classifier_index],
                                         number_of_trials=amount_trials)

        return JsonResponse(result)

    return HttpResponse(200)
