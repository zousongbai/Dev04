# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : pagination.py
# @Time         : 2020/7/16 15:49

# 导入PageNumberPagination
from rest_framework.pagination import PageNumberPagination

class MyPagination(PageNumberPagination):
    """重写PageNumberPagination类，对分页进行扩展"""
    # 指定默认每一页的数据的条数
    page_size=4
    # 设置前端指定页码的查询字符串的key的名称，如：指定多少页
    page_query_param='p'
    # 设置前端指定每一页数据条数的查询字符串key的名称，如：用s表示每一页显示的数据条数
    # 指定显示指定之后，前端才支持指定每一页的数据条数
    page_size_query_param='s'
    #指定最大的每一页的数据条数，如每一页最多显示50数据条数
    max_page_size=50