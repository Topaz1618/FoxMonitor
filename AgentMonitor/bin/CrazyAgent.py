#_*_coding:utf-8_*_
# Author:Topaz
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)

from core import main
if __name__ == "__main__":
    print("接下来")
    main.command_handler(sys.argv)
