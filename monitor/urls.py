#_*_coding:utf-8_*_
# Author:Topaz
from django.conf.urls import url

from  monitor import monitor_views

urlpatterns = [
    url(r'^triggers/$',monitor_views.triggers,name='triggers' ),
    url(r'hosts/$', monitor_views.hosts, name='hosts'),
    url(r'host_groups/$', monitor_views.host_groups, name='host_groups'),
    url(r'hosts/(\d+)/$', monitor_views.host_detail, name='host_detail'),
    url(r'trigger_list/$', monitor_views.trigger_list, name='trigger_list'),



]