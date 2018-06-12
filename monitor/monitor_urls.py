from django.conf.urls import url,include
from monitor import monitor_views
urlpatterns = [

    url(r'agent/config/(\d+)/$',monitor_views.agent_con),
    url(r'agent/put/$',monitor_views.put_data),
    url(r'graphs/$', monitor_views.graphs_generator, name='get_graphs'),#在host_detail.html里通过jQuery访问
    url(r'hosts/status/$', monitor_views.hosts_status, name='get_hosts_status'),
]