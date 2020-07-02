# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : urls.py
# @Time         : 2020/6/19 14:05

from django.urls import path

# 导入视图
from projects.views import index_page, index_page2
# 导入类视图
from projects.views import IndexPage

urlpatterns = [
    path('index/', index_page),
    path('index2/', index_page2),
    # 类视图定义路由
    # （1）path函数的第二个参数为类视图名.as_view()
    path('index3/<int:pk>/',IndexPage.as_view()),
    # 类名+as_view()：会自动根据请求方法去调用指定的实例方法
    # 如：是get请求就会自动去调用get实例方法
    # 可以使用<url类型转化器:路径参数名>

    path('index3/',IndexPage.as_view()),
]