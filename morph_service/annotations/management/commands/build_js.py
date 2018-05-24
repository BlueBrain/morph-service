'''Command building the frontend application when "manage.py runserver" in invoqued'''
from subprocess import call

from django.core.management.base import BaseCommand


def build_js():
    '''The build command'''
    call('(cd frontend && npm i && npm run build)', shell=True)


class Command(BaseCommand):
    '''The Command'''

    def handle(self, *args, **options):
        '''The handle'''
        build_js()
