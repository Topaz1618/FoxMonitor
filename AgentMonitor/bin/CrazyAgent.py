# -*- coding: utf-8 -*-
"""
Entry file.

"""

__version__ = '1.0'
__author__ = 'topaz1618@163.com'

import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import main


if __name__ == "__main__":
    main.CommandHandler(sys.argv)
