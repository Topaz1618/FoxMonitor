# Mymonitor
基于 Django 开发的分布式监控系统，参考zabbix,openfalcon架构，实现前端、后端、监控插件、画图、数据优化存储等

### 功能
- 系统和服务监控
- 数据采集
- 数据存储和优化
- 数据可视化
- 监控报警
- 报警处理
- 后台管理


### 环境
- Python 3
- Centos 7.4/Mac
- Redis
- Django

### 架构简要说明
```
├── AgentMonitor(client端)
├── monitor(核心代码)
├── static(静态文件)
├── handler(核心代码)
├── main.py(运行 Server)
├── static(静态文件)
├── templates(模板)
├── tests(测试文件)
├── README.md(项目说明)
└── requirements.txt(python库依赖)
```

### 安装与运行步骤

#### 服务端安装步骤
 - 下载MyMonitor
	从github下载最新版 MyMonitor 源码。
	git clone https://github.com/Topaz1618/MyMonitor.git
	cd MyMonitor/

 - 安装依赖项
	pip3 install -r requirements.txt

 - 使数据库状态与当前模型集和迁移集同步
 	python manage.py migrate

 - 创建管理用户
 	python manage.py createsuperuser

 - 运行
	python3 manage.py runserver 0.0.0.0:9000  启动监控服务web端

	python3 MonitorServer.py start  启动监控主程序

	python3 MonitorServer.py trigger_watch  启动报警监听程序

#### 客户端部署步骤
 - 安装依赖项

 	yum install gcc python-devel
 	pip3  install  psutil
 - 配置
 	cd AgentMonitor/
	vim  conf/settings.py
	configs = {
    	'HostID':1,						#clinet 端id 必须唯一
    	'ServerIp':'192.168.43.136',	#指向 server 端 ip
    	'ServerPort':'8007',			#指向 server 端 port
    }
 - 运行
 	python bin/CrazyAgent.py start


### 截图
1.主页面
![](https://github.com/Topaz1618/MyMonitor/blob/master/statics/unity/img/monitor.png)
2.主机页
![](https://github.com/Topaz1618/MyMonitor/blob/master/statics/unity/img/monitor2.png)
3.监控图
![](https://github.com/Topaz1618/MyMonitor/blob/master/statics/unity/img/monitor7.png)
![](https://github.com/Topaz1618/MyMonitor/blob/master/statics/unity/img/monitor6.png)


### 注意事项
1. 目前只支持 Python3

2. Mac 和 Linux 下可用，Windows 环境未测试


### LICENSE
开源协议：MPL

请遵守MPL协议，对Minos进行二次开发与使用。
