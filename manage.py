#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zdecydujmyrazem.settings")
    sys.path.insert(0, './dep')
    sys.path.insert(1, '/Library/Python/2.7/site-packages/')
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
