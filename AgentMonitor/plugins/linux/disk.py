#_*_coding:utf-8_*_
# Author:Topaz
import psutil
value_dic = {'part':{},'io':{}}
def monitor():
    parts = psutil.disk_partitions()    #磁盘全部信息
    disk_io = psutil.disk_io_counters() #磁盘io读写
    disk_parts_io = psutil.disk_io_counters(perdisk=True)
    value_dic['io']={
        'read_count':disk_io.read_count,
        'write_count':disk_io.write_count,
        'read_bytes':disk_io.read_bytes,
        'write_bytes ':disk_io.write_bytes,
    }
    for part in parts:
        usage = psutil.disk_usage(part.mountpoint)  #磁盘利用率
#        print(part.device,part.mountpoint,part.fstype,part.opts,usage.total,usage.used,usage.free,usage.percent)
        value_dic['part'][part.device] = {
            'device':part.device,
            'mountpoint':part.mountpoint,
            'fstype':part.fstype,
            'opts':part.opts,
            'usage':{
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent':usage.percent,
            }
        }
    '''
    监控单个分区io读写信息
    for part_io,message in disk_parts_io.items():
        print(part_io,message.read_count,message.read_bytes,message.write_count,message.write_bytes)
    '''
    return value_dic
if __name__ == "__main__":
    print(monitor())

