# MyMonitor
## 目录结构
    


## 实现功能
    client端主动获取监控项，执行插件，主动汇报数据
    Server端添加删除主机，模板，监控项，触发器，action
    server端存储数据到redis，根据表达式判断设置时间内的数据，触发则报警 
    前端显示监控主机详情，显示监控主机数据图等


## 启动
    python3 manage.py runserver 127.0.0.1:9000  启动监控服务web端
    python3 ServerMonitor.py start  启动监控主程序
    python3 ServerMonitor.py trigger_watch  启动报警监听程序
    
## 前端页面
     ![](https://github.com/Topaz1618/MyMonitor/blob/master/statics/unity/img/monitor.png)
     ![](https://github.com/Topaz1618/MyMonitor/blob/master/statics/unity/img/monitor2.png)
     ![](https://github.com/Topaz1618/MyMonitor/blob/master/statics/unity/img/monitor7.png)
     ![](https://github.com/Topaz1618/MyMonitor/blob/master/statics/unity/img/monitor6.png)
    
