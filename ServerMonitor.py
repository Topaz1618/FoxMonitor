# -*- coding: utf-8 -*-
"""
Server listener.

"""

__version__ = '1.0'
__author__ = 'topaz1618@163.com'

import os
import sys


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',"MyMonitor.settings")
    from monitor.backends.management import execute_from_command_line
    execute_from_command_line(sys.argv)