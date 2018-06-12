# from django.shortcuts import render
# from monitor import models
#
# # Create your views here.
# def dashboard(request):
#     return render(request, 'monitor/dashboard.html')
#
# def triggers(request):
#     return render(request,'monitor/triggers.html')
#
# def hosts(request):
#     host_list = models.Host.objects.all()
#     print('host',host_list)
#     return render(request,'monitor/hosts.html',{'host_list':host_list})
#
# def host_detail(request,host_id):
#     host_obj = models.Host.objects.get(id=host_id)
#     return render(request,'monitor/host_detail.html',{'host_obj':host_obj})
#
# def host_groups(request):
#     pass
#
#
# def trigger_list(request):
#     pass
