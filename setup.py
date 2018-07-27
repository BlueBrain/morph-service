#!/usr/bin/env python
""" Morph service module """
from subprocess import call

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install

from morph_service.version import VERSION

FRONTEND_INSTALL_CMD = '(cd morph_service/frontend && npm i && npm run build)'


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        call(FRONTEND_INSTALL_CMD, shell=True)
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        call(FRONTEND_INSTALL_CMD, shell=True)
        install.run(self)


REQS = ['Django==1.11.6',
        'django-cors-middleware==1.3.1',
        'neurom==2.0.0',
        'sklearn',
        'tmd>=1.0.2',
        'requests==2.18.4',
        'livereload==2.5.1']

TESTS_REQUIRE = [
    'argparse',
    'pep8==1.4.6',
    'nose==1.3.0',
    'django-nose==1.4.5',
    'nosexcover==1.0.8',
    'coverage==3.7',
    'astroid==1.6.3',
    'pylint==1.8.4',
    'django-nose==1.4.5',
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
      package_data={
          '': ['*.js'],
      },
      cmdclass={
          'develop': PostDevelopCommand,
          'install': PostInstallCommand,
      },
      dependency_links=[
          'git+ssh://bbpcode.epfl.ch/molecularsystems/TMD#egg=tmd-1.0.0',
          'git+https://git@github.com/wizmer/NeuroM.git@morphio#egg=neurom-2.0.0'
      ],
      scripts=['manage.py'],
      include_package_data=True)
