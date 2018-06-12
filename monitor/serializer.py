#_*_coding:utf-8_*_
# Author:Topaz
import json
import time
from monitor import models
from django.core.exceptions import  ObjectDoesNotExist

class AgentHandler(object):
    def __init__(self,client_id):
        self.client_id = client_id
        self.item_dic = {
            "items":{},
        }
    def get_configs(self):
        print("来取数据库配置啦")
        try:
            host_obj = models.Host.objects.get(id=self.client_id)
            templates_list = host_obj.template.select_related()
            for template in templates_list:
                for item in template.item.select_related():
                    self.item_dic['items'][item.name] = [item.interval]
                    # print('item',item)
        except ObjectDoesNotExist as e:
            print('抓到一个错误',e)
        return self.item_dic

    # def get_host_triggers(self,h_obj):
    #     pass


class GroupStatus(object):
    def __init__(self,request,RedisObj):
        self.request = request
        self.redis = RedisObj
    def by_hosts(self):
        host_data_list = []
        host_obj_list = models.Host.objects.all()
        for host in host_obj_list:
            host_data_list.append(self.get_all_status(host))
        return host_data_list

    def get_all_status(self,host_obj):
        '''
        生成一个这样的字典返回，包含如下内容
        1.基本信息：主机id，主机名，主机IP，上一次更新时间，
        2.trigger：拿到所有trigger，需要报警的去拿前面的报警字典
        data = {"id": 3, "ip": "10.0.0.138", "status": "Problem", "uptime": ''，"last_update": '', "ok_nums": '', "total_services": '', "name": "centos3",
        "triggers": {"1": [],
                     "2": [{"msg": "cpu io", "start_time": 1509211940.508585, "host_id": 3, "trigger_id": 1,
                    "positive_expressions": [{"calc_res_val": 8.291666666666666, "expression_obj": 1, "calc_res": 'true', "service_item": ''},{"calc_res_val": 91.07666666666667, "expression_obj": 2, "calc_res": 'true', "service_item": ''}], "time": "2017-10-29 02:58:53", "duration": 5193}],
                     "3": [],
                     "4": [{"msg": "Some thing must be wrong with client [10.0.0.138] , because haven't receive data of service [LinuxLoad] for [4890.764604568481]s (interval is [40])\u001b[0m", "start_time": 1509212306.696004, "host_id": 3, "trigger_id": '', "positive_expressions": '', "duration": 4832, "time": "2017-10-29 02:58:58"}],
                     "5": []},}
        '''
        host_data = {
            'id':host_obj.id,
            'hosts': host_obj.name,
            'ip':host_obj.ip,
            'status': host_obj.get_status_display(),
            'uptime': None,
            'last_update':None,
            'total_services':None,
            'ok_nums':None,
        }
        # print('##@$##%$#%',host_obj.get_status_display(),host.status)
        uptime = self.get_host_uptime(host_obj)
        if uptime:
            host_data['uptime'] = uptime[0]['uptime']
            host_data['last_update'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(uptime[1]))
        host_data['triggers'] = self.get_triggers(host_obj)
        return host_data

    def get_host_uptime(self, host_obj):
        redis_key = 'Data_%s_uptime_latest' % host_obj.id
        last_data_point = self.redis.lrange(redis_key, -1, -1)
        if last_data_point:
            last_data_point, last_update = json.loads(last_data_point[0])
            return last_data_point, last_update
    def get_triggers(self,host_obj):
        trigger_keys = self.redis.keys("host_%s_trigger_*" % host_obj.id)
        trigger_dic = {
            1 : [],
            2 : [],
            3 : [],
            4 : [],
            5 : []
        }
        for trigger_key in trigger_keys:
            trigger_data = self.redis.get(trigger_key)
            print("trigger_key",trigger_key)
            if trigger_key.decode().endswith("None"):
                trigger_dic[4].append(json.loads(trigger_data.decode()))
            else:
                '''!!!!这里要改下，需要再来改'''
                trigger_id = trigger_key.decode().split('_')[-1]
                trigger_obj = models.Trigger.objects.get(id=trigger_id)
                trigger_dic[trigger_obj.severity].append(json.loads(trigger_data.decode()))
        return trigger_dic



# host_list = models.Host.objects.all()
# for host in host_list:
#     item_list = []
#     # key_list = []
#     template_list = host.template.select_related()
#     host_data['hosts'].append(host.id)
#     for template in template_list:
#         item_list.extend(template.item.all())
#     for item in item_list:
#         host_data['items'].append(item.name)
#     # key_list.extend(item.keys.all())
#     # for key in key_list:
#     #    expression_list = key.triggerexpression_set.select_related()
#     #    for expression in expression_list:
#     #        trigger_list = expression.trigger_set.select_related()
#     data_set.append(host_data)


