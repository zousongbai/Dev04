# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : urls.py
# @Time         : 2020/6/19 14:05

from django.urls import path

# 导入视图
from projects.views import index_page, index_page2

urlpatterns = [
    path('index/', index_page),
    path('index2/', index_page2)

]