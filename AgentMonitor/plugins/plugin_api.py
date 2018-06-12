#_*_coding:utf-8_*_
# Author:Topaz
# from linux import cpu
import time
from plugins.linux import memory,disk,cpu,network,load,mysql

def LinuxCpu():
    return cpu.monitor()

def LinuxMemory():
    return memory.monitor()

def LinuxDisk():
    return disk.monitor()

def LinuxNetwork():
    return network.monitor()

def LinuxLoad():
    return load.monitor()

def Mysql():
    return mysql.MyssqlMonitor().get_value()

