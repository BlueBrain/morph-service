'''A backend that return a validation report for a given morphology'''
import numpy as np
import neurom as nm
from neurom import NeuriteType, load_neuron, iter_sections, iter_segments, iter_neurites
from neurom.check import CheckResult
from neurom.core.dataformat import COLS

from neurom.check.neuron_checks import (
    has_no_dangling_branch, has_no_root_node_jumps, has_no_jumps, has_no_narrow_start,
    has_no_fat_ends, has_all_nonzero_segment_lengths, has_no_narrow_neurite_section)


def has_no_radical_diameter_changes(neuron, max_change=10):
    '''Check if the neuron is radical diameter changes
    Arguments:
        neuron(Neuron): The neuron object to test
        max_change(float): The maximum percentage of variation allowed per um.
            example: max_change=2 means the diameter cannot vary more than 2% per um

    Returns:
        CheckResult with result. result.info contains a list of (section Id, position)
        where radical diameter changes happen
    '''
    bad_ids = list()
    for section in iter_sections(neuron):
        for p0, p1 in iter_segments(section):  # pylint: disable=invalid-name
            length = np.linalg.norm(p0[COLS.XYZ] - p1[COLS.XYZ])
            relative_change = abs(p0[COLS.R] - p1[COLS.R]) / (p0[COLS.R] + p1[COLS.R])
            if relative_change / length > (max_change / 100.):
                bad_ids.append((section.id, p1))
    return CheckResult(len(bad_ids) == 0, bad_ids)


def has_no_single_child(neuron):
    '''Check if the neuron has sections with only one child
    Arguments:
        neuron(Neuron): The neuron object to test

    Returns:
        CheckResult with result. result.info contains a list of (section Id, section end position)
        for each section with a single child
    '''

    bad_ids = list()
    for section in iter_sections(neuron):
        if len(section.children) == 1:
            bad_ids.append((section.id, section.points[-1, COLS.XYZ]))
    return CheckResult(len(bad_ids) == 0, bad_ids)


def has_no_multifurcation(neuron):
    '''Check if the neuron has sections with only one child
    Arguments:
        neuron(Neuron): The neuron object to test

    Returns:
        CheckResult with result. result.info contains a list of (section Id, section end position)
        for each section with more than 2 children
    '''

    bad_ids = list()
    for section in iter_sections(neuron):
        if len(section.children) > 2:
            bad_ids.append((section.id, section.points[-1, COLS.XYZ]))
    return CheckResult(len(bad_ids) == 0, bad_ids)


def validation_report(filename):
    '''Return the payload that will be sent back to the user'''
    neuron = load_neuron(filename)

    return {
        'neurites': {
            'dangling_branch': len(has_no_dangling_branch(neuron).info),
            'root_node_jump': len(has_no_root_node_jumps(neuron).info),
            'z_jumps': len(has_no_jumps(neuron, axis='z').info),
            # has_no_radical_diameter_changes
            'narrow_start': len(has_no_narrow_start(neuron, frac=0.9).info),
            'fat_ends': len(has_no_fat_ends(neuron).info),
            'has_all_nonzero_segment_lengths': len(has_all_nonzero_segment_lengths(neuron).info),
            'narrow_neurite_section': len(has_no_narrow_neurite_section(neuron,
                                                                        neurite_filter=None).info),
        },

        'bifurcations': {
            'single_child': len(has_no_single_child(neuron).info),
            'multifurcation': len(has_no_multifurcation(neuron).info),
        },

        'dendrites': {
            # Apical dendrite annotated for pyramidal cell = boolean (A)
            'number_of_dendritic_trees_steaming_from_the_soma': len([
                neurite for neurite in iter_neurites(neuron)
                if neurite.type in {NeuriteType.basal_dendrite, NeuriteType.apical_dendrite}]),
        },

        'axons': {
            'number_of_axons': len([neurite for neurite in iter_neurites(neuron)
                                    if neurite.type == NeuriteType.axon]),
            # Correct start point of the axon (or axons if there are 2) = boolean (A)
        },

        'additional_features': {
            'max_branch_order': int(max(nm.features.get('section_branch_orders', neuron))),
            'total_section_length': float(nm.features.get('total_length', neuron)[0]),
            'max_section_length': float(max(nm.features.get('section_lengths', neuron))),
        }
    }
