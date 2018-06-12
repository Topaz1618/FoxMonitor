#_*_coding:utf-8_*_
# Author:Topaz


configs = {
    'HostID':1,
    'ServerIp':'192.168.1.159',
    'ServerPort':'8008',
    'urls':{
        'get_configs':['api/agent/config','get'],
        'put_data':['api/agent/put/','post'],
    },
    'Timeout':30,
    'ConfigUpdateInterval':300,
}