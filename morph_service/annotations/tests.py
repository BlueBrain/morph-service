'''Contains annotation test'''
import os
import json
import unittest
from django.test import Client

from neurom.io import load_neuron


PATH = os.path.dirname(__file__)

class SimpleTest(unittest.TestCase):
    '''Annotation test'''

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        '''Issue a GET request.'''
        with open('morph_service/annotations/sample.asc') as inputf:
            response = self.client.post('/annotations/api', {'attachment': inputf})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        file_content = ''.join(data['file'])
        neuron = load_neuron(file_content, reader='asc')
        self.assertEqual(len(neuron.neurites), 2)

        got_annotations = '\n'.join(file_content.split('\n')[-7:])
        self.assertEqual(got_annotations,
                         """(Circle2   ; MUK_ANNOTATION
    (Color Green)   ; MUK_ANNOTATION
    (Name "zjump")   ; MUK_ANNOTATION
    (      6.00      13.00       0.00 0.50)   ; MUK_ANNOTATION
    (      6.00      13.00      50.00 0.50)   ; MUK_ANNOTATION
)   ; MUK_ANNOTATION
""")

        with open('morph_service/annotations/sample.swc') as outf:
            response = self.client.post('/annotations/api', {'attachment': outf})
        self.assertEqual(response.status_code, 400, 'SWC files should return 400')

    def test_single_children(self):
        '''Issue a GET request.'''
        with open(os.path.join(PATH, 'single_children.asc')) as inputf:
            response = self.client.post('/annotations/api', {'attachment': inputf})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        file_content = ''.join(data['file'])
        annotation = """(Circle7   ; MUK_ANNOTATION
    (Color Red)   ; MUK_ANNOTATION
    (Name "single children")   ; MUK_ANNOTATION
    (      0.00      13.00       0.00 0.50)   ; MUK_ANNOTATION
)   ; MUK_ANNOTATION"""

        actual = '\n'.join(file_content.split('\n')[-7:]).strip()
        self.assertEqual(actual,
                         annotation)


    def test_multifurcation(self):
        '''Issue a GET request.'''
        with open(os.path.join(PATH, 'multifurcation.asc')) as inputf:
            response = self.client.post('/annotations/api', {'attachment': inputf})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        file_content = ''.join(data['file'])
        annotation = """(Circle8   ; MUK_ANNOTATION
    (Color Yellow)   ; MUK_ANNOTATION
    (Name "Multifurcation")   ; MUK_ANNOTATION
    (      0.00      13.00       0.00 0.50)   ; MUK_ANNOTATION
)   ; MUK_ANNOTATION"""

        self.assertEqual('\n'.join(file_content.split('\n')[-6:]).strip(),
                         annotation)
