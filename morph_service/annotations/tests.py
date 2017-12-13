'''Contains annotation test'''
import json
import unittest
from io import StringIO

from django.test import Client

from neurom.io import load_neuron


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
        neuron = load_neuron(StringIO(file_content), reader='asc')
        self.assertEqual(len(neuron.neurites), 2)
        annotation = """(Circle2   ; MUK_ANNOTATION
    (Color Green)   ; MUK_ANNOTATION
    (Name "zjump")   ; MUK_ANNOTATION
    (6.0 13.0 0.0 0.50)   ; MUK_ANNOTATION
    (6.0 13.0 50.0 0.50)   ; MUK_ANNOTATION
)   ; MUK_ANNOTATION
"""
        self.assertEqual('\n'.join(file_content.split('\n')[-7:]),
                         annotation)

        with open('morph_service/annotations/sample.swc') as outf:
            response = self.client.post('/annotations/api', {'attachment': outf})
        self.assertEqual(response.status_code, 400, 'SWC files should return 400')
