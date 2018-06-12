#_*_coding:utf-8_*_
# Author:Topaz
from core import client

class command_handler(object):
    '''分拣命令'''
    def __init__(self,comm):
        self.comm = comm
        self.check()

    def check(self):
        if len(self.comm) < 2:
            print("滚犊子")
        else:
            if hasattr(self,self.comm[1]):
                func = getattr(self,self.comm[1])
                func()
            else:
                print("找错人了吧呵呵")

    def start(self):
        print("开始获取 item 数据")
        Client = client.ClientHandle()
        Client.forever_run()



    def stop(self):
        print("stop")
