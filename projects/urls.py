# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : urls.py
# @Time         : 2020/6/19 14:05

from django.urls import path

# 导入类视图
from projects import views

urlpatterns = [
    path('projects/',views.ProjectsView.as_view()),
    path('projects/<int:pk>/',views.ProjectDetailView.as_view()),
]
# 1、url设计的时候，有时候要传递id，有时候不需要传递id，怎样解决
# 2、为什么需要在路径中传递pk参数？好处是什么？
# （1）好处一：它帮我们做了一层校验，只要能够到视图里面说明pk一定是正整数