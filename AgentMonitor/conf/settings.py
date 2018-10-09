#_*_coding:utf-8_*_
"""
Client configuration

"""

__version__ = '1.0'
__author__ = 'topaz1618@163.com'

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