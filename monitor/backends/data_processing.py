#_*_coding:utf-8_*_
# Author:Topaz
import time
import json
import sys
from monitor import models
from monitor.backends import my_redis
import operator


class DataHandler(object):
    '''
    1.获取监控配置
    2.根据获取到的时间检查服务主机是否按时汇报
    3.调用redis发布没有按时汇报的，并存储在redis里5分钟以供计数使用
    '''
    def __init__(self,django_settings):
        self.settings = django_settings
        self.last_loading_time = 0
        self.update_interval = 20
        self.load_sleep = 5
        self.monitor_dic = {}
        self.redis = my_redis.redis_conn(django_settings)

    def looping(self):
        print("hello looping")
        self.update_configs()
        while True:
            if time.time() - self.last_loading_time >= self.update_interval:
                print("去更新配置噜")
                self.update_configs()
            print('!!!!!',self.monitor_dic)
            if self.monitor_dic:
                for h,config_dic in self.monitor_dic.items():
                    print('====>look at here',h,config_dic)
                    for item_id,val in config_dic['items'].items():
                        item_obj,monitor_time = val
                        if time.time() - monitor_time >= item_obj.interval:
                            self.monitor_dic[h]['items'][item_obj.id][1] = time.time()
                            self.data_validation(h,item_obj)
            # print(self.monitor_dic)
            time.sleep(self.load_sleep)

    def update_configs(self):
            '''load monitor config from Mysql DB'''
            print("取监控配置")
            host_list = models.Host.objects.all()
            for h in host_list:
                if h not in self.monitor_dic:
                    self.monitor_dic[h] = {'items':{},'expressions':{},'triggers':{}}
                item_list = []
                expression_list = []
                for template in h.template.select_related():
                    # print(template.item.select_related())
                    item_list.extend(template.item.select_related())
                    for item in template.item.select_related():
                        for key in item.keys.select_related():
                            expression_list.extend(key.triggerexpression_set.select_related())  ##alex这里添加了 trigger_list ，而我的trigger_list不和模板关联，和key关联
                for item in item_list:
                    if item.id not in self.monitor_dic[h]['items']:
                        self.monitor_dic[h]['items'][item.id] = [item,0]
                    else:
                        self.monitor_dic[h]['items'][item.id][0] = item
                for expression in expression_list:
                        self.monitor_dic[h]['expressions'][expression.id] = expression
                        trigger_obj = expression.trigger_set.select_related()
                        for trigger in trigger_obj:
                            self.monitor_dic[h]['triggers'][trigger.name] = trigger
            self.monitor_dic[h].setdefault('status_last_check', time.time())
            self.last_loading_time = time.time()
            # print('公共字典：%s' %self.monitor_dic)

    def data_validation(self,h,item_obj):
        '''数据汇报情况检查
        1.是否有数据汇报
        2.数据汇报是否超时
        3.超时主机状态设置成problem)
        '''
        redis_key = "Data_%s_%s_latest" %(h.id,item_obj.name)
        # print(redis_key)
        last_point = self.redis.lrange(redis_key,-1,-1)
        # print(last_point)
        if last_point:
            last_point = json.loads(last_point[0].decode())
            save_data,save_time = last_point
            # print(save_data,save_time)
            total_timeout = item_obj.interval + self.settings.ALLOWED_TIMEOUT
            if time.time() - save_time > total_timeout:
                data_timeout = time.time() - (save_time + total_timeout)
                msg = '''Message : The  host [%s] [%s] item has timed out [%s]seconds ''' %(h.ip, item_obj.name,data_timeout )
                self.trigger_notifier(h=h,msg=msg,trigger_name=None,expressions=None)
                #这里应该加个主机汇报状态检测，跟其他服务一个套路，所以偷个懒不写了，以后再完善
                h.status = 5  # 看眼models ,5就是设置成 problem
                h.save()
        else:
            msg = '''no data for item [%s] host[%s] at all..''' % (item_obj.name, h.name)
            self.trigger_notifier(h=h,msg=msg, trigger_name=None, expressions=None)
            h.status = 5  # 看眼models ,5就是设置成 problem
            h.save()

    def trigger_notifier(self,h,msg=None,trigger_name=None, expressions=None,redis_obj=None):
        '''1.报错消息发布到redis
            2.并在redis内存储5分钟(存储的目的是计数，所以不需要存储太久)
            3.两次及以上的报错计算出错误出现的时间并存储'''
        if redis_obj:
            self.redis = redis_obj  #外部调用这个函数时，可能传入了redis连接，避免重复调用
        print("hello trigger")
        msg_dic = {'host_id': h.id,
                   'trigger_name': trigger_name,
                   'msg': msg,
                   'expressions': expressions,  # 实例
                   'start_time': time.time(),
                   'current_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                   'duration': None     #出错了多久了
                   }
        self.redis.publish(self.settings.TRIGGER_CHANNEL,json.dumps(msg_dic)) #redis订阅/发布,这个是发布了一条消息
        trigger_key = "host_%s_trigger_%s" %(h.name,trigger_name)
        previous_data = self.redis.get(trigger_key)
        if previous_data:       #报警两次以上，要设置duration，就是这个错误已经出现多长时间了
            previous_data = previous_data.decode()
            start_trigger = json.loads(previous_data)['start_time']
            msg_dic['start_time'] = start_trigger
            msg_dic['duration'] = round(time.time() - start_trigger)
        # print('消息字典',msg_dic['duration'])
        # 同时在redis中纪录这个trigger , 前端页面展示时要统计trigger 个数
        self.redis.set(trigger_key, json.dumps(msg_dic), 300) #记录个数而已，每个trigger记录5分钟后自动清除
        # print("去存储")

    def wtf(self,h,redis_obj):
        '''
        :param h:
        :param redis_obj:
        1.调用函数ExpressionProcess拿到每条表达式里function的结果
        2.把为True(有问题的),保存到列表 alarm_expressions 里
        3.eval 计算出每个表达式里function结果的总和,计算出表达式结果的总和
        4.结果为True就调用监控
        '''
        try:
            self.redis = redis_obj
            if not self.monitor_dic:
                self.update_configs()
            trigger_dic = self.monitor_dic[h]['triggers']  #取出当前主机汇报主机的所有触发器
            for trigger_name,trigger_obj in trigger_dic.items():
                expression_str = ''
                alarm_expressions = []
                expression_list = trigger_obj.expression.select_related()
                for expression_obj in expression_list:
                    function_dic = expression_obj.function.select_related()
                    function_dic_len = len(function_dic)
                    function_str = ''
                    count = 0
                    for function in function_dic:       #在function里取出数据处理方式avg/max/min
                        count += 1
                        data_calc_func = function.data_calc_func
                        expression_handle = ExpressionProcess(self,h,expression_obj,data_calc_func,function)
                        single_expression_handle = expression_handle.handle()
                        if single_expression_handle:
                            if function_dic_len > 1 and function_dic_len > count:
                                function_str += str(single_expression_handle['calc_res']) + ' and' + ' '
                            else:
                                function_str += str(single_expression_handle['calc_res'])
                            if single_expression_handle and single_expression_handle['calc_res'] == True:
                                # calc_sub_res_list.append(single_expression_handle)
                                # if single_expression_handle['calc_res'] == True:
                                single_expression_handle['expression_obj'] = expression_obj.id
                                alarm_expressions.append(single_expression_handle)
                    need = eval(function_str)
                    if expression_obj.logic_type:
                        expression_str += str(need) + ' ' + expression_obj.logic_type + ' '
                    else:
                        expression_str += str(need) + ' '
                if expression_str:
                    trigger_res = eval(expression_str)
                    if trigger_res:
                        self.trigger_notifier(h,trigger_name=trigger_name,expressions=alarm_expressions)
        except:
            err = sys.exc_info()
            print("ERROR:data_pro 来人呀%s行有错误%s"%(err[2].tb_lineno,err[1]))


class ExpressionProcess(object):
    '''拿到每一条function的结果True/False，返回字典res_dic  #这个其实应该每个表达式一返回结果，以后改
    1.取出当前监控项的redis_key
    2.根据redis_key取出触发器设置时间内的数据
    3.计算出一定时间内数据的min/max/avg值
    4.跟阈值作比较,得到True/False
    '''
    def __init__(self,data_handler,h,expression_obj,data_calc_func,function):
        self.data_handler = data_handler
        self.data_calc_func = data_calc_func
        self.function_name = function.name
        self.operator_type = function.operator_type
        self.threshold = function.threshold
        self.host_obj = h
        self.expression_obj = expression_obj
        self.set_time = 10   #function表里少加了一条时间，这里就先假装是1吧
        self.point_list = []
        # print('检查',data_calc_func,self.function_name)
    def get_point(self):
        '''1.拼接出redis key，
        2.取出item的interval
        3.以上两项保存在列表里，用于接下来取数据'''
        #根据key取trigger obj
        # trigger_list = self.expression_obj.trigger_set.select_related()
        # for trigger_obj in trigger_list:
        #     trigger_name = trigger_obj.name
        #根据key取item object
        key_obj = self.expression_obj.keys.select_related()
        for key in key_obj:
            item_obj = key.item_set.select_related()
            for item in item_obj:
                item_name = item.name
                self.point_list.append(item.interval)
        redis_key = "Data_%s_%s_latest" %(self.host_obj.id,item_name)
        self.point_list.append(redis_key)
    def handle(self):
        '''1.调用函数get_point,得到列表
        2.调用取数据函数，根据1的列表得到数据列表
        3.根据数据处理方式找到不同函数，给数据列表给它处理'''
        try:
            if not self.point_list:
                self.get_point()
            data_list = self.load_data()
            if hasattr(self,'get_%s' %self.data_calc_func):
                func = getattr(self,'get_%s' %self.data_calc_func)
                single_expression_calc_res = func(data_list)
                if single_expression_calc_res:
                    res_dic = {
                    'calc_res':single_expression_calc_res[0],
                    'calc_res_val':single_expression_calc_res[1],
                    'expression_obj':self.expression_obj,
                    'item_item':single_expression_calc_res[2],
                    }
                    return res_dic
                else:
                    return False
            else:
                print("滚蛋，没有")
        except:
            err = sys.exc_info()
            print("ERROR:来人呀 data_pro %s行有错误%s"%(err[2].tb_lineno,err[1]))


    def load_data(self):
        #根据表达式的配置从redis加载数据,这个配置指的时间
        if not self.get_point:
            print("不行哦，没有拿到key")
            self.get_point()
        item_interval = self.point_list[0]
        redis_key = self.point_list[1]
        dirty_time = int(self.set_time) * 60
        dirty_point = int(dirty_time + 60) / int(item_interval)
        dirty_data = self.data_handler.redis.lrange(redis_key,-int(dirty_point),-1)
        dirty_data_list = [json.loads(i.decode())for i in dirty_data]
        # print('数据列表',dirty_data_list)
        data_list = []
        for point in dirty_data_list:
            save_data,save_time = point
            # print(222222,type(save_time))
            if time.time() - save_time < dirty_time:    #代表数据有效
                data_list.append(point)
        return data_list
    def get_avg(self,data_list):
        try:
            clean_data_list = []
            for data in data_list:
                val,time = data
                if val:
                    for k,v in val.items():
                        if k in self.function_name:
                            clean_data_list.append(float(val[k]))
            if clean_data_list:
                # print('喵',clean_data_list)
                avg_res = sum(clean_data_list) / len(clean_data_list)
                return [self.judge(avg_res), avg_res, None]
            else:  # 可能是由于最近这个服务 没有数据 汇报 过来,取到的数据 为空,所以没办法 判断阈值
                return [False, None, None]
        except:
            err = sys.exc_info()
            print("ERROR:来人呀 data_pro %s行有错误%s"%(err[2].tb_lineno,err[1]))

    def get_max(self,data_list):
        try:
            for data in data_list:
                val,save_time = data
            else:#可能是由于最近这个服务 没有数据 汇报 过来,取到的数据 为空,所以没办法 判断阈值
                return [False,None,None]
        except:
            err = sys.exc_info()
            print("ERROR:来人呀 data_pro %s行有错误%s"%(err[2].tb_lineno,err[1]))

    def judge(self,avg_res):
        '''
        :param avg_res:
        :return: True/False
        '''
        try:
            calc_func = getattr(operator,self.operator_type)
        except:
            err = sys.exc_info()
            print("ERROR:来人呀 data_pro %s行有错误%s"%(err[2].tb_lineno,err[1]))
        return calc_func(avg_res,self.threshold)


