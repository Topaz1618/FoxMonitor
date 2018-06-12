#_*_coding:utf-8_*_
# Author:Topaz
import psutil
value_dic ={'data':{}}
def monitor():
    devices_message = psutil.net_io_counters(pernic=True)   #每个网络接口的io信息
    for device_name,device_message in devices_message.items():
        value_dic['data'][device_name] = {
            'bytes_sent':device_message.bytes_sent,
            'bytes_recv':device_message.bytes_recv,
            'packets_sent':device_message.packets_sent,
            'packets_recv':device_message.packets_recv,
        }
    return value_dic
if __name__ == "__main__":
   print(monitor())
'''
{'lo': {'bytes_sent': 27500, 'packets_sent': 550, 'bytes_recv': 27500, 'packets_recv': 550},
 'eth0': {'bytes_sent': 16348937, 'packets_sent': 101563, 'bytes_recv': 211450177, 'packets_recv': 211928}}
'''