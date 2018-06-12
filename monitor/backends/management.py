#_*_coding:utf-8_*_
# Author:Topaz
import sys
import os
import django
django.setup()
from django.conf import settings
from monitor.backends import data_processing
from monitor.backends import trigger_handler
class ManagementUtility(object):
    def __init__(self,argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        print('看看拿到啥了',self.argv)
        self.argv_check()

    def argv_check(self):
        if len(self.argv) < 2:
            print("没传参")
        else:
            comm = self.argv[1]
            if hasattr(ManagementUtility,comm):
                print("有这个")
                func = getattr(ManagementUtility,comm)
                func()
            else:
                print("滚犊子没这人")
    @staticmethod
    def start():
        print("start")
        catty = data_processing.DataHandler(settings)
        catty.looping()
    @staticmethod
    def stop():
        print("stop")
        return "stop"
        # print("结束了吗")

    @staticmethod
    def trigger_watch():
        print('trigger')
        trigger_watch = trigger_handler.TriggerHandler(settings)
        trigger_watch.start_watching()

def execute_from_command_line(argv=None):
    '''A simple method that runs a ManagementUtility'''
    ManagementUtility(argv)