#!/usr/bin/env python
"""
C-academy richie management script.
"""
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cacademy.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Development")

    from configurations.management import execute_from_command_line  # noqa

    execute_from_command_line(sys.argv)
