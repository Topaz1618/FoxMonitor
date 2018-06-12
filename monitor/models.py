from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class HostGroup(models.Model):
    '''主机组'''
    name = models.CharField(max_length=64,unique=True)
    def __str__(self):
        return self.name

class Host(models.Model):
    '''主机'''
    name = models.CharField(max_length=64,unique=True)
    ip = models.GenericIPAddressField(unique=True)
    host_alive = models.IntegerField('主机存活状态监测',default=30)
    enabled = models.BooleanField(default=True)
    status_choices = ((1,'Online'),
        (2,'Down'),
        (3,'Unreachable'),
        (4,'Offline'),
        (5,'Problem'),
    )
    status = models.IntegerField(choices=status_choices,default=1)
    host_group = models.ManyToManyField('Host',blank=True)
    template = models.ManyToManyField('Template',blank=True)
    def __str__(self):
        return self.name

class Template(models.Model):
    '''模板'''
    name = models.CharField(max_length=64,unique=True)
    item = models.ManyToManyField('Item',blank=True)
    def __str__(self):
        return self.name

class Trigger(models.Model):
    '''触发器'''
    name = models.CharField(max_length=64)
    severity_choices = ((0,'Not classified'),
                        (1, 'Information'),
                        (2, 'Warning'),
                        (3,'Average'),
                        (4, 'High'),
                        (5,'Disaster'))

    severity = models.IntegerField(choices=severity_choices,default=2)
    expression = models.ManyToManyField('TriggerExpression',max_length=64)
    enable = models.BooleanField(default=True,verbose_name="已启用")
    def __str__(self):
        return self.name

class TriggerExpression(models.Model):
    '''表达式'''
    # items = models.ManyToManyField("Item")
    keys = models.ManyToManyField("Key")
    # test = models.CharField(choices=test_choices)
    function = models.ManyToManyField("Function")
    logic_type_choices = (('or', 'OR'), ('and', 'AND'))
    logic_type = models.CharField(u"与一个条件的逻辑关系", choices=logic_type_choices, max_length=32, blank=True, null=True)
    def __str__(self):
        for i in self.function.all():
            return "%s %s(%s(%s))" % (i.data_calc_func, i.name,i.operator_type, i.threshold)
        return "%s %s %s" %(self.keys,self.function,self.logic_type)

class Function(models.Model):
    '''数据处理'''
    data_calc_type_choices = (
        ('avg', 'Average'),
        ('max', 'Max'),
        ('hit', 'Hit'),
        ('last', 'Last'))
    data_calc_func = models.CharField(u"数据处理方式", choices=data_calc_type_choices, max_length=64)
    name = models.CharField(max_length=64, unique=True)
    operator_type_choices = (('eq', '='), ('lt', '<'), ('gt', '>'))
    operator_type = models.CharField(u"运算符", choices=operator_type_choices, max_length=32)
    threshold = models.IntegerField(u"阈值")
    def __str__(self):
        return "%s %s(%s(%s))" %(self.data_calc_func,self.name,self.operator_type,self.threshold)

class Item(models.Model):
    '''项目'''
    name = models.CharField(max_length=64,unique=True)
    interval = models.IntegerField(default=60,verbose_name="监控间隔")
    monitor_by_choices = (
        ('agent','Agent'),
        ('snmp','SNMP'),
        ('wget','WGET'),
    )    #通信方式
    monitored_by = models.CharField(max_length=64,choices=monitor_by_choices)
    data_choices = (
        ('int','int'),
        ('float','float'),
        ('str','str')
    )
    data_type = models.CharField(choices=data_choices,max_length=64)
    keys = models.ManyToManyField('Key')
    def __str__(self):
        return self.name

class Key(models.Model):
    '''键值'''
    name = models.CharField(max_length=64)
    def __str__(self):
        return "%s" %(self.name)

class UserProfile(models.Model):
    '''用户'''
    user = models.OneToOneField(User,models.CASCADE)
    name = models.CharField(max_length=64,blank=True)
    def __str__(self):
        return self.name

class Action(models.Model):
    '''动作'''
    name = models.CharField(max_length=64, unique=True)
    triggers = models.ManyToManyField('Trigger', blank=True, help_text=u"想让哪些trigger触发当前报警动作")
    operations = models.ManyToManyField('ActionOperation', verbose_name="报警动作")
    interval = models.IntegerField(u'告警间隔(s)', default=300)
    recover_notice = models.BooleanField(u'故障恢复后发送通知消息', default=True)
    enabled = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class ActionOperation(models.Model):
    '''报警动作：名字，报警步骤，报警类型，通知对象，通知格式'''
    name = models.CharField(max_length=64, verbose_name="Name")
    step_from = models.IntegerField(verbose_name="Step from")
    step_to = models.IntegerField(verbose_name="Step to")
    action_type_choices = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('script', 'RunScript'),
    )
    action_type = models.CharField(u"动作类型", choices=action_type_choices, default='email', max_length=64)
    send_to_user = models.ManyToManyField('UserProfile', verbose_name=u"通知对象", blank=True)
    _msg_format = '''Host({hostname},{ip}) service({service_name}) has issue,msg:{msg}'''
    msg_format = models.TextField(u"消息格式", default=_msg_format)
    def __str__(self):
        return self.name
