# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import unittest
from django.test import TestCase
from django.test import Client

class SimpleTest(unittest.TestCase):
    '''Annotation test'''

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        '''Issue a GET request.'''
        with open(os.path.join(os.path.dirname(__file__), 'simple.asc')) as inputf:
            response = self.client.post('/converter/api',
                                        {'output_extension': '.swc', 'file': inputf})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content,
                         '# index     type         X            Y            Z       radius       parent\n1           1     0.000000     0.000000     0.000000     1.000000          -1\n2           3     0.000000     0.000000     0.000000     1.000000           1\n3           3     0.000000     5.000000     0.000000     1.000000           2\n4           3    -5.000000     5.000000     0.000000     1.500000           3\n5           3     6.000000     5.000000     0.000000     1.500000           3\n6           2     0.000000     0.000000     0.000000     1.000000           1\n7           2     0.000000    -4.000000     0.000000     1.000000           6\n8           2     6.000000    -4.000000     0.000000     2.000000           7\n9           2    -5.000000    -4.000000     0.000000     2.000000           7\n\n# Created by MorphIO v1.0.3\n')


        with open(os.path.join(os.path.dirname(__file__), 'simple.asc')) as inputf:
            r = self.client.post('/converter/api',
                                        {'output_extension': '.h5', 'file': inputf})

        with open('/tmp/test.h5', 'wb') as f:
            f.write(r.content)

        self.assertEqual(False, True)
