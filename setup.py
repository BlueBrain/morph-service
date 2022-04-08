#!/usr/bin/env python
""" Morph service module """
from subprocess import check_call
from setuptools import find_packages, setup
from setuptools.command import sdist
from morph_service.version import VERSION


def js_prerelease(command):
    """decorator for building minified js/css prior to another command """
    class DecoratedCommand(command):
        '''The decorator'''

        def run(self):
            '''The run function'''
            check_call('cd morph_service/frontend && npm i && npm run build'
                       ' && cp -R dist ../static', shell=True)

            command.run(self)
            update_package_data(self.distribution)
    return DecoratedCommand



def update_package_data(distribution):
    """update package_data to catch changes during setup"""
    build_py_ = distribution.get_command_obj('build_py')
    # distribution.package_data = find_package_data()
    # re-init build_py options which load package_data
    build_py_.finalize_options()


REQS = ['Django==1.11.17',
        'django-cors-middleware==1.5.0',
        'morph-tool==2.3.0',
        'sklearn',
        'neurom==2.0.1.dev6',
        'tmd==2.0.9',
        'morphio==2.6.1',
        'requests>=2.18.4',
        'livereload>=2.5.1']

TESTS_REQUIRE = [
    'argparse',
    'pep8>=1.4.6',
    'nose>=1.3.0',
    'nosexcover>=1.0.8',
    'coverage>=3.7',
    'astroid>=1.6.3',
    'pylint>=1.8.4',
    'django-nose>=1.4.5',
]

setup(name='morph-service',
      version=VERSION,
      description='morphology service',
      packages=find_packages(),
      author='bbp platform team',
      author_email='bbp-ou-nse@epfl.ch',
      license='BBP-internal-confidential',
      url='http://bluebrain.epfl.ch',
      install_requires=REQS,
      tests_require=TESTS_REQUIRE,
      extras_require={
          'extension_tests': TESTS_REQUIRE,
      },
      cmdclass={
          'sdist': js_prerelease(sdist.sdist),
      },
      dependency_links=[
      ],
      scripts=['manage.py'],
      include_package_data=True)
