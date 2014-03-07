#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zdecydujmyrazem.settings")
    sys.path.insert(0, './dep')
    sys.path.insert(0, '/Library/Python/2.7/site-packages/')
    sys.path.insert(0, '/Users/dwa/src/ZdecydujmyRazem/zdecydujmy-razem/ZDENV/lib/python2.7/site-packages/')
    sys.path.insert(0, '/Users/dwa/src/django-notification-fork/django-notification')
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
