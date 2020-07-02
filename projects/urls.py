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
# url设计的时候，有时候要传递id，有时候不需要传递id，怎样解决