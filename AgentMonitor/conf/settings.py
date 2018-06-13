#_*_coding:utf-8_*_
# Author:Topaz


configs = {
    'HostID':1,
    'ServerIp':'127.0.0.1',
    'ServerPort':'8007',
    'urls':{
        'get_configs':['api/agent/config','get'],
        'put_data':['api/agent/put/','post'],
    },
    'Timeout':30,
    'ConfigUpdateInterval':300,
}