#_*_coding:utf-8_*_
# Author:Topaz
from django.core.mail import send_mail
from monitor.backends import my_redis
from django.conf import settings
from monitor import models
import json
import time

class TriggerHandler(object):
    def __init__(self,django_settings):
        self.django_settings = django_settings
        self.redis = my_redis.redis_conn(self.django_settings)
        self.alert_counters = {}
        print("hello ")
    def start_watching(self):
        print("start watching ")
        radio = self.redis.pubsub()
        radio.subscribe(self.django_settings.TRIGGER_CHANNEL)
        radio.parse_response()
        self.trigger_count = 0
        while True:
            msg = radio.parse_response()
            self.trigger_consume(msg)
    def trigger_consume(self,msg):
        self.trigger_count += 1
        trigger_msg = json.loads(msg[2].decode())
        # print('来啊放纵啊',trigger_msg)
        action = ActionHandler(trigger_msg,self.alert_counters)
        action.action_handler()

class ActionHandler(object):
    def __init__(self,trigger_msg,alert_counters):
        self.trigger_msg = trigger_msg
        self.alert_counters = alert_counters

    def action_handler(self):
        #在data_validation里,item汇报超时或者主机没有拿到数据
        if self.trigger_msg.get('trigger_name') == None:
            pass
            # print("Item汇报超时/主机没有拿到数据")
        else:
            print("正经报错")
            host_id = self.trigger_msg.get('host_id')
            trigger_name = self.trigger_msg.get('trigger_name')
            print(host_id,trigger_name)
            trigger_obj = models.Trigger.objects.get(name=trigger_name)
            action_list = trigger_obj.action_set.select_related()
            matched_action_list = set()
            for action in action_list:
                for trigger in action.triggers.select_related():
                    print('Trigger',trigger.name)
                    if trigger_name == trigger.name:
                        matched_action_list.add(action)
                        if action.id not in self.alert_counters:
                            self.alert_counters[action.id] = {}
                        if host_id not in self.alert_counters[action.id]:
                            self.alert_counters[action.id][host_id] = {'counter': 0, 'last_alert': time.time()}
                        else:
                            if time.time() - self.alert_counters[action.id][host_id]['last_alert'] > action.interval:
                                self.alert_counters[action.id][host_id]['counter'] += 1
                            else:
                                pass
                print("action",action)
            #     print(action.name)
            print('拿到了什么',self.alert_counters)
            for action in matched_action_list:
                if time.time() - self.alert_counters[action.id][host_id]['last_alert'] >= action.interval:
                    operation_list = action.operations.select_related()
                    for operation in operation_list:
                        step = operation.step_to
                        if self.alert_counters[action.id][host_id]['counter'] <= step:
                            action_func = getattr(self, 'action_%s' % operation.action_type)
                            action_func(action,operation,host_id,self.trigger_msg)
                            self.alert_counters[action.id][host_id]['last_alert'] = time.time()
                            break

    def action_email(self,action,operation,host_id,trigger_msg):
        '''
        :param action:
        :param operation:
        :param host_id:
        :param trigger_msg:
        :return:
        '''
        mail_list = [ user_email  for user_email in operation.send_to_user.all()]
        msg =   '级别:%s -- 主机:%s -- 服务:%s' %(trigger_msg.get('trigger_name'),
                                              trigger_msg.get('host_id'),
                                              trigger_msg.get('expressions'))
        print("看看报警内容",msg)
        send_mail(
            msg,
            operation.msg_format,
            settings.DEFAULT_FROM_EMAIL,
            mail_list,
        )


    def action_script(self,action,operation,host_id,trigger_msg):
        print("脚本")



