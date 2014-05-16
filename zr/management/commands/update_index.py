__author__ = 'dwa'
import os, os.path
from django.core.management.base import BaseCommand, CommandError
from zr import index

class Command(BaseCommand):
    help = 'Update app index'

    def handle(self, *args, **options):
        self.stdout.write('Updating index...')
        index.create_new_index()
        self.stdout.write('... done!')

