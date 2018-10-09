# -*- coding: utf-8 -*-
"""
Client configuration

"""

__version__ = '1.0'
__author__ = 'topaz1618@163.com'

from core import client


class CommandHandler(object):
    def __init__(self,comm):
        self.comm = comm
        self.check()

    def check(self):
        """ Check command.

        :return:
        """
        if len(self.comm) < 2:
            self.help_document()
            return
        else:
            if hasattr(self,self.comm[1]):
                func = getattr(self,self.comm[1])
                func()
            else:
                print("Command does not exist. ")

    def help_document(self):
        """

        :return:
        """
        # TODO
        msg = """
        Usage: xxxx
        
        """
        print(msg)

    def start(self):
        """
        Start the client listener

        :param start:
        :return
        """
        # TODO add log
        Client = client.ClientHandle()
        Client.forever_run()



    def stop(self):
        """
        Stop the client listener

        :param stop:
        :return
        """
        pass
        # TODO add log
