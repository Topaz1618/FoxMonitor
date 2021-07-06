<img src='statics/unity/img/FoxMonitor.png' width='380' title='FoxMonitor, A distributed monitoring system'>

A distributed monitoring system developed based on Django, with reference to Zabbix, Open-Falcon architecture, to achieve front-end, back-end, monitoring plug-ins, drawing, data optimized storage, etc.  By [Topaz](https://topaz1618.github.io/about)([Website](http://topazaws.com/)|[Blog](https://topaz1618.github.io/blog/))

[Chinese README](https://github.com/Topaz1618/FoxMonitor/blob/master/README_CN.markdown)

## Features
- System and service monitoring
- Data collection
- Data storage and optimization
- Data visualization
- Monitoring alarm
- Alarm handling
- Backstage management

## Environment
- Python 3.6.5
- Django
- Redis
- Centos 7.4/Mac

## Installation
### Server side installation

1. Download FoxMonitor

```
 $git clone https://github.com/Topaz1618/FoxMonitor.git
 $cd FoxMonitor/
```

2.Install dependencies
```
 pip3 install -r requirements.txt
```

3.Create user & sync data
```
 - Synchronize the database
 python manage.py migrate

 - Create admin user
 python manage.py createsuperuser
```

4.Modify configuration
```
 $cd MyMonitor
 $vim settings.py
  REDIS_CONN = {
      'HOST':'10.0.0.129',
      'PORT':6379,
      'DB':0,
 }
```

5.Run
```
 python3 manage.py runserver 0.0.0.0:9000  // Start the web side of the monitoring service

 python3 MonitorServer.py start  // Start the monitoring main program

 python3 MonitorServer.py trigger_watch  // Start the alarm listener program
```


### Client side installation

1.Install dependencies
```
 yum install gcc python-devel
 pip3  install  psutil
```

2.Configuration
```
 $cd AgentMonitor/
 $vim  conf/settings.py
 configs = {
   	'HostID':1,						#clinet 端id 必须唯一
   	'ServerIp':'192.168.43.136',	#指向 server 端 ip
   	'ServerPort':'8007',			#指向 server 端 port
 }
```
3.Run
```
 python bin/CrazyAgent.py start
```

## Screenshots

### 【Main Page】
![](https://github.com/Topaz1618/MyMonitor/blob/master/statics/unity/img/monitor.png)

### 【List Of All Hosts】
![](https://github.com/Topaz1618/MyMonitor/blob/master/statics/unity/img/monitor2.png)

### 【Monitoring Chart】
![](https://github.com/Topaz1618/MyMonitor/blob/master/statics/unity/img/monitor7.png)
![](https://github.com/Topaz1618/MyMonitor/blob/master/statics/unity/img/monitor6.png)


## Precautions
- Available under Mac and Linux, not tested in Windows environment

## License
Licensed under the MIT license
