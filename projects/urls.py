# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : urls.py
# @Time         : 2020/6/19 14:05

from django.urls import path
# 导入类视图
from projects import views


urlpatterns = [
    # （1）继承ViewSet之后，支持在定义路由时指定请求方法与action的映射
    # （2）as_view需要接收一个字典
    # （3）key为请求方法名，value为指定需要调用的action
    path('projects/',views.ProjectsViewSet.as_view(
        {   # 请求方法与指定的action一一映射
            'get':'list',
            'post':'create',
        }
    )),

    path('projects/names/',views.ProjectsViewSet.as_view(
        {   # 请求方法与指定的action一一映射
            'get':'names', # 指定get方法请求，并且url是projects/names/就会访问names

        }
    )),

    path('projects/<int:pk>/',views.ProjectsViewSet.as_view(
        {
            # 请求方法与指定的action一一映射
            'get':'retrieve',
            'put':'update',
            'delete':'destroy',
        }
    )),

    # 获取项目的接口数据
    path('projects/<int:pk>/interfaces/',views.ProjectsViewSet.as_view(
        {
            # 请求方法与指定的action一一映射
            'get':'interfaces'
        }
    )),
]
# url设计的时候，有时候要传递id，有时候不需要传递id，怎样解决