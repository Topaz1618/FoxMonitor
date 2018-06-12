#_*_coding:utf-8_*_
# Author:Topaz
import psutil
def monitor():
    mem = psutil.virtual_memory()
    mem_swap = psutil.swap_memory()
    mem_dic = { 'MemTotal': mem.total,
            'MemUsage': mem.used,
            'Cached': mem.cached,
            'MemFree':mem.free ,
            'Buffers': mem.buffers,
            'SwapFree': mem_swap.free,
            'SwapUsage': mem_swap.used,
            'SwapTotal': mem_swap.total,
            }
    return mem_dic
if __name__ == '__main__':
    print(monitor())
