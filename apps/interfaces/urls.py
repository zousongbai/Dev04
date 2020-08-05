# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : urls.py
# @Time         : 2020/6/19 14:05

# 导入类视图
from . import views
# 导入路由器
from rest_framework.routers import SimpleRouter

# 定义SimpleRouter路由对象　
router = SimpleRouter()

# 使用路由对象.register()方法，来进行注册
router.register(r'interfaces', views.InterfacesViewSet)

urlpatterns = [

]

# 使用路由对象.urls属性来获取自动生成的路由条目，往往为列表
# 需要将这个列表添加到urlpatterns
urlpatterns += router.urls
