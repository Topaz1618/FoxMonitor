#_*_coding:utf-8_*_
# Author:Topaz
from monitor import models
from django.conf import settings
import json
from django.http import HttpResponse

class GraphGenerator(object):
    '''
    产生图片
    '''
    def __init__(self,request,redis_obj):
        self.request = request
        self.redis = redis_obj
        self.host_id = self.request.GET.get('host_id')
        self.time_range = self.request.GET.get('time_range')    #默认是latest
        # print(11111111111111,self.request,self.host_id,self.time_range)


    def get_host_graph(self):
        item_data_dic = {}
        host_obj = models.Host.objects.get(id=self.host_id)
        templates_list = list(host_obj.template.select_related())
        for template in templates_list:
            for item in template.item.select_related():
                # print(item.id,item.name)
                item_data_dic[item.id] ={
                    'name': item.name,
                    'index_data': {},
                    'raw_data': [],
                    'keys': [key.name for key in item.keys.all()],
                }
        # service_redis_key = "Data_%s_%s_%s" % (self.host_id,[name])
        for item_id,val_dic in item_data_dic.items():
            redis_key = "Data_%s_%s_%s" % (self.host_id,val_dic['name'],self.time_range)
            raw_data = self.redis.lrange(redis_key, 0, -1)
            service_raw_data = [item.decode() for item in raw_data]
            item_data_dic[item_id]['raw_data'] = service_raw_data

        # print('字典', item_data_dic)
        return item_data_dic