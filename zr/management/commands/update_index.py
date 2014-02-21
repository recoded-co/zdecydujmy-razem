__author__ = 'dwa'
import os, os.path
from django.core.management.base import BaseCommand, CommandError
from zr.index import Index

class Command(BaseCommand):
    help = 'Update app index'

    def handle(self, *args, **options):
        self.stdout.write('Updating index...')
        index = Index()
        index.update_index()
        self.stdout.write('... done!')

