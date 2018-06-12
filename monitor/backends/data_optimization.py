#_*_coding:utf-8_*_
# Author:Topaz
from django.conf import settings
import json
import time
import copy
import sys

class DataStore(object):
    '''优化+存储监控数据到redis'''
    def __init__(self,data,client_id,item_name,RedisObj):
        self.data = data
        self.client_id = client_id
        self.item_name = item_name
        self.redis_obj = RedisObj
        self.processing_to_save()

    def processing_to_save(self):
        print("hello ,数据存储+优化开始噜",settings.REDIS_CONFIGS)
        try:
            for k,v in settings.REDIS_CONFIGS.items():
                optimize_interval,save_point = v
                redis_key = "Data_%s_%s_%s" %(self.client_id,self.item_name,k)
                # print('拼接出来的key',redis_key)
                last_point = self.redis_obj.lrange(redis_key,-1,-1)
                if not last_point:
                    self.redis_obj.rpush(redis_key,json.dumps([None,time.time()]))
                if optimize_interval == 0:
                    self.redis_obj.rpush(redis_key,json.dumps([self.data,time.time()]))
                else:
                    previous_data,previous_time =json.loads(self.redis_obj.lrange(redis_key,-1,-1)[0].decode())
                    if time.time() - previous_time > optimize_interval:
                        # print("超时了，准备优化数据噜")
                        latest_key = "Data_%s_%s_latest" %(self.client_id,self.item_name)
                        dirty_data = self.data_slice(latest_key,optimize_interval)
                        if len(dirty_data) > 0:
                            # print("拿到需要的数据了，接下来去计算优化结果，数据长度：",len(dirty_data))
                            optimize_data = self.get_optimize_data(redis_key,dirty_data)
                            if optimize_data:
                                self.save_optimize_data(redis_key, optimize_data)
                if self.redis_obj.llen(redis_key) >= save_point:
                    print("长啦",self.redis_obj.llen(redis_key))
                    self.redis_obj.lpop(redis_key)
        except:
            err = sys.exc_info()
            print("hello data_optimization %s行有错误%s"%(err[2].tb_lineno,err[1]))

    def data_slice(self,latest_key,optimize_interval):
        '''
        取出给定时间内的所有数据，供接下来优化使用
        :param latest_key:
        :param optimize_interval:
        :return:
        '''
        # print("开始优化 Key:%s 优化间隔:%s" %(latest_key,optimize_interval))
        all_data = self.redis_obj.lrange(latest_key,1,-1)
        dirty_data_list = []
        # print('已有数据',all_data)
        for preparation_data in all_data:
            real_data = json.loads(preparation_data.decode())
            if len(real_data) == 2:
                save_data,save_time = real_data
                if time.time() - save_time >= optimize_interval:
                    # print("    == 时间区间 %s 内的数据 %s" %(optimize_interval,real_data))
                    dirty_data_list.append(real_data)
                else:
                    pass
        return dirty_data_list

    def get_optimize_data(self,redis_key,dirty_data):
        #给定时间内的数据，计算出平均值，最大值，最小值，中间值并返回
        try:
            item_key = dirty_data[0][0].keys()
            first_point = dirty_data[0][0]
            optimize_dic = {}
            if 'data' not in item_key:
                # print("妹有data",redis_key,item_key)
                for key in item_key:
                    optimize_dic[key] = []
                tmp_dic = copy.deepcopy(optimize_dic)
                # print('临时列表',tmp_dic)
                for item,item_time in dirty_data:
                    for item_key1,val in item.items():
                        if val == 'up':
                            print('1111',item_key1,type(val))
                        tmp_dic[item_key1].append(round(float(val),2))
                for k,v_list in tmp_dic.items():
                    c = self.get_res(v_list)
                    optimize_dic[k] = [c]
                print('已优化数据：',optimize_dic)
            else:
                '''网卡优化'''
                for k1,v1 in first_point['data'].items():
                    optimize_dic[k1] = {}
                    for k2,v2 in v1.items():
                        optimize_dic[k1][k2] = []
                tmp_dic = copy.deepcopy(optimize_dic)
                if tmp_dic:
                    for save_data,save_time in dirty_data:
                        for k1,v1 in save_data['data'].items():
                            for k2,v2 in v1.items():
                                tmp_dic[k1][k2].append(round(float(v2),2))
                    for k1,v_dic in tmp_dic.items():
                        for k2,v_list in v_dic.items():
                            c = self.get_res(v_list)
                            optimize_dic[k1][k2] = [c]
                print('网卡优化之后', optimize_dic)
        except:
            err = sys.exc_info()
            print("ERROR:来人呀data_op %s行有错误%s"%(err[2].tb_lineno,err[1]))
        return optimize_dic

    def get_res(self,v_list):
        '''
        :param v_list:
        :return: 获取到的监控数据在一定时间内的平均值，最大值，最小值，中间值
        '''
        avg_res = self.get_average(v_list)
        max_res = self.get_max(v_list)
        min_res = self.get_min(v_list)
        mid_res = self.get_mid(v_list)
        return avg_res,max_res,min_res,mid_res
    def get_average(self,v_list):
        if len(v_list) >0:
            return round(sum(v_list) /len(v_list),2)
        else:
            return 0
    def get_max(self,v_list):
        if len(v_list) >0:
            return max(v_list)
        else:
            return 0
    def get_min(self,v_list):
        if len(v_list) >0:
            return min(v_list)
        else:
            return 0
    def get_mid(self,v_list):
        v_list.sort()
        if len(v_list) > 0:
            return v_list[int(len(v_list)/2)]
        else:
            return 0

    def save_optimize_data(self, redis_key, optimize_data):
        #存储优化后的数据
        self.redis_obj.rpush(redis_key, json.dumps([optimize_data, time.time()]))















