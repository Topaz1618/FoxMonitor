#_*_coding:utf-8_*_
# Author:Topaz
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse
# from monitor import serializer
from monitor.serializer import AgentHandler
from monitor.backends import my_redis
from monitor.backends import data_optimization
from monitor.backends import data_processing
from monitor import serializer
from django.conf import settings
from monitor import models
from monitor import graphs
import time
import json
import sys

RedisObj = my_redis.redis_conn(settings)
# print('Redis Status',RedisObj.set("catty",time.ctime()))

def agent_con(request,agent_id):
    agent_obj = AgentHandler(agent_id)
    config = agent_obj.get_configs()
    if config:
        print('config==>',config)
        return  HttpResponse(json.dumps(config))
        # return json.dumps(config)

@csrf_exempt
def put_data(request):
    if request.method == "POST":
        try:
            # print('request',request.POST.get('client_id'),request.POST.get('item_name'),request.POST.get('data'))
            data = json.loads(request.POST.get('data'))
            client_id = request.POST.get('client_id')
            item_name = request.POST.get('item_name')
            print('===>data', data,'===>client_id',client_id,'==>item_name',item_name)
            data_optimization.DataStore(data,client_id,item_name,RedisObj)  #来了数据就去存起来
            print('Redis Status', RedisObj.set("catty", time.ctime()))
            #同时触发trigger检查
            expressions_handler = data_processing.DataHandler(settings)
            h= models.Host.objects.get(id=client_id)
            expressions_handler.wtf(h,RedisObj)
        # except Exception as e:
        except:
            err = sys.exc_info()
            print("ERROR:来人呀%s行有错误%s"%(err[2].tb_lineno,err[1]))
    return HttpResponse("行了收到你的数据了")

@login_required
def hosts(request):
    host_list = models.Host.objects.all()
    print("hosts:",host_list)
    return render(request,'monitor/hosts.html',{'host_list':host_list})

@login_required
def dashboard(request):
    return render(request, 'monitor/dashboard.html')

@login_required
def profile(request):
    return render(request,'monitor/基本信息.html')

@login_required
def host_detail(request,host_id):
    host_obj = models.Host.objects.get(id=host_id)
    print(host_obj)
    return render(request, 'monitor/host_detail.html',{'host_obj':host_obj})
    # return render(request, 'monitor/graph.html',{'host_obj':host_obj})

@login_required
def hosts_status(request):
    hosts_data_list = []
    host_status= serializer.GroupStatus(request,RedisObj)
    hosts_data = host_status.by_hosts()
    print('前端所需数据',hosts_data)
    return HttpResponse(json.dumps(hosts_data))

@login_required
def triggers(request):
    return render(request, 'monitor/triggers.html')

@login_required
def host_groups(request):
    return render(request, 'monitor/triggers.html')

@login_required
def trigger_list(request):
    return render(request, 'monitor/triggers.html')

@login_required
def graphs_generator(request):
    print(request.GET.get('client_id'))
    graphs_generator = graphs.GraphGenerator(request,RedisObj)
    graphs_data = graphs_generator.get_host_graph()
    print("graphs_data", graphs_data)
    return  HttpResponse(json.dumps(graphs_data))

@login_required
def test(request):
    #(login_url='/admin/login/?next=/admin/')
    # return HttpResponse('nihao')
    return render(request, 'monitor/test/2.html')


