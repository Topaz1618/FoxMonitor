#_*_coding:utf-8_*_
# Author:Topaz
import psutil
def monitor(frist_invoke=1):
    cpu_message = psutil.cpu_times()
    value_dic= {
        'user': cpu_message.user,
        'nice': cpu_message.nice,
        'system': cpu_message.system,
        'idle': cpu_message.idle,
}
    return value_dic
if __name__ == '__main__':
    print(monitor())
