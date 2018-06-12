#_*_coding:utf-8_*_
# Author:Topaz
import subprocess
class MyssqlMonitor(object):
    def __init__(self):
        self.user = 'topaz'
        self.passwd = '123456'
        self.value_dic = {}
    def get_value(self):
        key_list = ['Com_insert', 'Com_update', 'Com_delete', 'Com_select']
        for key in key_list:
            temp, last = subprocess.getstatusoutput(
                "mysqladmin -u%s -p%s extended-status|grep '\<%s\>'|cut -d'|' -f3"
                %(self.user,self.passwd,key))
#            print(temp,last)

            if key == 'Com_insert':
                self.value_dic['insert'] = int(last)
            elif key == 'Com_update':
                self.value_dic['update'] = int(last)
            elif key == 'Com_delete':
                self.value_dic['delete'] = int(last)
            else:
                self.value_dic['select'] = int(last)
        self.mysql_tps()
        self.mysql_qps()
        return self.value_dic
    def mysql_tps(self):
        tps = self.value_dic['insert'] +self.value_dic['update'] + self.value_dic['delete']
        self.value_dic['tps'] = tps
    def mysql_qps(self):
        qps = self.value_dic['insert'] +self.value_dic['update'] + self.value_dic['delete'] + self.value_dic['select']
        self.value_dic['qps'] = qps
if __name__ == "__main__":
    MyssqlMonitor().get_value()
