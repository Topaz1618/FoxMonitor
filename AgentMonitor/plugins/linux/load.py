#_*_coding:utf-8_*_
# Author:Topaz

import subprocess
def monitor():
    shell_command = 'uptime'
    status,result = subprocess.getstatusoutput(shell_command)
    load1,load5,load15 = result.split('load average:')[1].split(',')
    #print(load1,load5,load15)
    value_dic= {
            'load1': load1,
            'load5': load5,
            'load15': load15,
    }
    return value_dic
if __name__ == "__main__":
    print(monitor())
