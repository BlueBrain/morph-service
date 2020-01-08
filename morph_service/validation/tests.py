'''Test of the validation service'''
import os
import json
import re
import unittest
from django.test import Client

from neurom.io import load_neuron


PATH = os.path.dirname(__file__)

class SimpleTest(unittest.TestCase):
    '''Annotation test'''

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def _test_validation(self, response, expected):
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertDictEqual(data, expected)

    def test_details(self):
        '''Issue a GET request.'''
        with open('morph_service/annotations/sample.asc') as inputf:
            response = self.client.post('/validation/api', {'attachment': inputf})
        self.maxDiff = None
        self._test_validation(response, {'additional_features': {'max_branch_order': 1,
                                                                 'max_section_length': 65.94427490234375,
                                                                 'total_section_length': 83.94427490234375},
                                         'axons': {'number_of_axons': 1},
                                         'bifurcations': {'multifurcation': 0, 'single_child': 0},
                                         'dendrites': {'number_of_dendritic_trees_steaming_from_the_soma': 1},
                                         'neurites': {'dangling_branch': 0,
                                                      'fat_ends': 0,
                                                      'has_all_nonzero_segment_lengths': 0,
                                                      'z_jumps': 1,
                                                      'narrow_neurite_section': 0,
                                                      'narrow_start': 0,
                                                      'root_node_jump': 2}})

        with open('morph_service/annotations/sample.swc') as inputf:
            response = self.client.post('/validation/api', {'attachment': inputf})
        self._test_validation(response, {'additional_features': {'max_branch_order': 10,
                                                                 'max_section_length': 11.758281707763672,
                                                                 'total_section_length': 840.6852240562439},
                                         'axons': {'number_of_axons': 1},
                                         'bifurcations': {'multifurcation': 0, 'single_child': 0},
                                         'dendrites': {'number_of_dendritic_trees_steaming_from_the_soma': 3},
                                         'neurites': {'dangling_branch': 0,
                                                      'fat_ends': 0,
                                                      'has_all_nonzero_segment_lengths': 0,
                                                      'narrow_neurite_section': 0,
                                                      'narrow_start': 3,
                                                      'root_node_jump': 0,
                                                      'z_jumps': 0}})

        with open('morph_service/validation/no-neurites.swc') as inputf:
            response = self.client.post('/validation/api', {'attachment': inputf})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode('utf-8'))
        self.assertTrue(re.match('Error: no-neurites\w*.swc has no neurites', data['error']),
                        'Error checking: {}'.format(data['error']))

        with open('morph_service/validation/no-soma.swc') as inputf:
            response = self.client.post('/validation/api', {'attachment': inputf})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode('utf-8'))
        self.assertTrue(re.match('Error: no-soma\w*.swc has no soma', data['error']),
                        'Error checking: {}'.format(data['error']))
