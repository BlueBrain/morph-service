#!/usr/bin/env python
""" Morph service module """
from setuptools import setup, find_packages
from morph_service.version import VERSION

REQS = ['Django==1.11.6',
        'livereload==2.5.1',
        'neurom']

TESTS_REQUIRE = [
    'argparse',
    'pep8',
    'nose',
    'nosexcover',
    'coverage',
    'astroid',
    'pylint',
    'django-nose',
    ]

setup(name='morph-service',
      version=VERSION,
      description='morphology service',
      packages=find_packages(exclude=[]),
      author='bbp platform team',
      author_email='bbp-ou-nse@epfl.ch',
      license='BBP-internal-confidential',
      url='http://bluebrain.epfl.ch',
      install_requires=REQS,
      tests_require=TESTS_REQUIRE,
      extras_require={
          'extension_tests': TESTS_REQUIRE,
      },
      scripts=['manage.py'],
      include_package_data=True,)
