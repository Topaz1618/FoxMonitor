#_*_coding:utf-8_*_
# Author:Topaz
import time
from conf import settings
import urllib
import urllib.request
import urllib.parse
import  json
import threading
from plugins import plugin_api

class ClientHandle(object):
    def __init__(self):
        self.agent_data = {}

    def update_configs(self):
        print('hello')
        request_type = settings.configs['urls']['get_configs'][1]
        url = "%s/%s" %(settings.configs['urls']['get_configs'][0],settings.configs['HostID'])
        get_configs = self.url_request(request_type,url)
        print(get_configs)
        get_configs = json.loads(get_configs.decode())
        self.agent_data.update(get_configs)


    def forever_run(self):
        last_update_time = 0
        while True:
            if time.time() - last_update_time > settings.configs['ConfigUpdateInterval']:
                print("该更新噜")
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
                    print(" --- hold on %ss which %s monitor" %(agent_interval - (time.time() - last_time ),item))
            time.sleep(60)


    def invoke_plugin(self,item,val):
        if hasattr(plugin_api,item):
            func = getattr(plugin_api,item)
            callback = func()
            # print(callback)
            post_data = {
                'client_id':settings.configs['HostID'],
                'item_name':item,
                'data':json.dumps(callback)
            }
            rtype = settings.configs['urls']['put_data'][1]
            url = settings.configs['urls']['put_data'][0]
            self.url_request(rtype,url,params=post_data)
        else:
            print("没这监控插件，滚蛋儿吧")

    def url_request(self,rtype,url,**extra_data):
        abs_url = "http://%s:%s/%s" % (settings.configs['ServerIp'],
                                       settings.configs["ServerPort"],
                                       url)
        print('请求的url',abs_url)
        if rtype in ('get','GET'):
            try:
                # req = urllib.request.Request(abs_url)
                req_data = urllib.request.urlopen(abs_url)
                configs = req_data.read()
                return configs
            except Exception as e:
                print("抓到错误",e)
        elif rtype in ('post','POST'):
            try:
                print('传数据噜',extra_data['params'])
                data_encode = urllib.parse.urlencode(extra_data['params'])
                data_encode = bytes(data_encode.encode('utf-8'))
                req = urllib.request.Request(url=abs_url,data=data_encode)
                req_data = urllib.request.urlopen(req,timeout=settings.configs['Timeout'])
                callback = req_data.read()
                print('ok',callback.decode())
            except Exception as e:
                print("抓到一个错误",e)