#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    #sys.path.insert(0, '/Users/dwa/src/ZdecydujmyRazem/zdecydujmy-razem/ZDENV/lib/python2.7/site-packages/')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zdecydujmyrazem.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
