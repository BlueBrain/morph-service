# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import unittest
from django.test import TestCase
from django.test import Client

from numpy.testing import assert_array_equal

from morphio import Morphology
from morph_tool import diff

class SimpleTest(unittest.TestCase):
    '''Annotation test'''

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        '''Issue a GET request.'''

        input_filename = os.path.join(os.path.dirname(__file__), 'simple.asc')
        with open(os.path.join(os.path.dirname(__file__), 'simple.asc')) as inputf:
            response = self.client.post('/converter/api',
                                        {'output_extension': '.swc', 'file': inputf})

        self.assertEqual(response.status_code, 200)

        swc_name = '/tmp/blah.swc'
        with open(swc_name, 'wb') as f:
            f.write(response.content)

        self.assertFalse(diff(input_filename, swc_name))

        with open(os.path.join(os.path.dirname(__file__), 'simple.asc')) as inputf:
            r = self.client.post('/converter/api',
                                 {'output_extension': '.h5', 'file': inputf})

        h5_name = '/tmp/blah.h5'

        with open(h5_name, 'wb') as f:
            f.write(r.content)
        self.assertFalse(diff(input_filename, h5_name))
