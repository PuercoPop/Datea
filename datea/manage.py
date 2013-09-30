#!/usr/bin/env python
import os
import sys
import settings.base

sys.path.insert(0, settings.base.APP_PATH, )
sys.path.insert(0, settings.base.PROJECT_PATH)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
