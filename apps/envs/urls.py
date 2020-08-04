# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : urls.py
# @Time         : 2020/6/19 14:05

from django.urls import path
# 导入类视图
from . import views
# 导入路由器
from rest_framework.routers import DefaultRouter, SimpleRouter

# 定义SimpleRouter路由对象　
router = SimpleRouter()
router.register(r'envs', views.EnvsViewSet)
# prefix：路由前缀，如：r'projects/'
# viewset：视图集，如：views.ProjectsViewSet
urlpatterns = [

]

urlpatterns += router.urls
