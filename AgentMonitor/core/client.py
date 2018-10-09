# -*- coding: utf-8 -*-
"""
Entry file.

"""

__version__ = '1.0'
__author__ = 'topaz1618@163.com'

import time
import  json
import urllib
import urllib.request
import urllib.parse
import threading

from conf import settings
from plugins import plugin_api


class ClientHandle(object):
    """

    """
    def __init__(self):
        self.agent_data = {}

    def update_configs(self):
        """

        :return:
        """
        request_type = settings.configs['urls']['get_configs'][1]
        url = "%s/%s" %(settings.configs['urls']['get_configs'][0],settings.configs['HostID'])
        get_configs = self.url_request(request_type,url)
        get_configs = json.loads(get_configs.decode())
        self.agent_data.update(get_configs)


    def forever_run(self):
        """

        :return:
        """
        last_update_time = 0
        while True:
            if time.time() - last_update_time > settings.configs['ConfigUpdateInterval']:
                self.update_configs()
                last_update_time = time.time()
            for item,val in self.agent_data['items'].items():
                if len(val) == 1:
                    self.agent_data['items'][item].append(0)
                agent_interval = val[0]
                last_time = val[1]
                if time.time() - last_time > agent_interval:
                    self.agent_data['items'][item][1] = time.time()
                    t = threading.Thread(target=self.invoke_plugin,args=(item,val))
                    t.start()
                    print("going to monitor %s~" %item)
                else:
                    print(" hold on %ss which %s monitor" %(agent_interval - (time.time() - last_time ),item))
            time.sleep(60)


    def invoke_plugin(self,item,val):
        """

        :param item:
        :param val:
        :return:
        """
        if hasattr(plugin_api,item):
            func = getattr(plugin_api,item)
            callback = func()
            post_data = {
                'client_id':settings.configs['HostID'],
                'item_name':item,
                'data':json.dumps(callback)
            }
            rtype = settings.configs['urls']['put_data'][1]
            url = settings.configs['urls']['put_data'][0]
            self.url_request(rtype,url,params=post_data)
        else:
            print("Monitoring plugin does not exist. ")

    def url_request(self,rtype,url,**extra_data):
        """

        :param rtype:
        :param url:
        :param extra_data:
        :return:
        """
        abs_url = "http://%s:%s/%s" % (settings.configs['ServerIp'],
                                       settings.configs["ServerPort"],
                                       url)
        if rtype in ('get','GET'):
            try:
                req_data = urllib.request.urlopen(abs_url)
                configs = req_data.read()
                return configs
            except Exception as e:
                pass
                # TODO: add log
        elif rtype in ('post','POST'):
            try:
                data_encode = urllib.parse.urlencode(extra_data['params'])
                data_encode = bytes(data_encode.encode('utf-8'))
                req = urllib.request.Request(url=abs_url,data=data_encode)
                req_data = urllib.request.urlopen(req,timeout=settings.configs['Timeout'])
                callback = req_data.read()
                print('ok',callback.decode())
            except Exception as e:
                pass
                # TODO: add log