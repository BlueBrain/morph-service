import os
import unittest
from io import StringIO
from tempfile import NamedTemporaryFile

from django.test import Client, TestCase
from neurom.io import load_neuron


class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        with open('annotations/sample.asc') as fp:
            response = self.client.post('/annotations/api', {'attachment': fp})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        n = load_neuron(StringIO(response.content.decode('utf-8')), reader='asc')
        self.assertEqual(len(n.neurites), 2)
        annotation = """(Circle2   ; MUK_ANNOTATION
    (Color Green)   ; MUK_ANNOTATION
    (Name "zjump")   ; MUK_ANNOTATION
    (6.0 13.0 0.0 0.50)   ; MUK_ANNOTATION
    (6.0 13.0 50.0 0.50)   ; MUK_ANNOTATION
)   ; MUK_ANNOTATION
"""
        self.assertEqual('\n'.join(response.content.decode('utf-8').split('\n')[-7:]),
                         annotation)

        with open('annotations/sample.swc') as fp:
            response = self.client.post('/annotations/api', {'attachment': fp})
        self.assertEqual(response.status_code, 400)
