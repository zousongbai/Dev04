# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : pagination.py
# @Time         : 2020/7/16 15:49

# 导入PageNumberPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class MyPagination(PageNumberPagination):
    """重写PageNumberPagination类，对分页进行扩展"""
    # 指定默认每一页的数据的条数
    page_size=10
    # 设置前端指定页码的查询字符串的key的名称，如：指定多少页
    page_query_param='p'
    # 设置前端指定每一页数据条数的查询字符串key的名称，如：用s表示每一页显示的数据条数
    # 指定显示指定之后，前端才支持指定每一页的数据条数
    page_size_query_param='size'
    #指定最大的每一页的数据条数，如每一页最多显示50数据条数
    max_page_size=50
    page_query_description = '第几页'
    page_size_query_description = '每页几条'

    def get_paginated_response(self, data):
        # 方法二：对父类进行拓展
        response = super().get_paginated_response(data)
        response.data['current_page_num'] = self.page.number
        response.data['total_pages'] = self.page.paginator.num_pages
        return response

        # # 方法一：重写父类（不推荐使用，因为需要导入很多依赖包）
        # # 当前页数
        # current_page_num = self.page.number
        # # 总的页数
        # total_pages = self.page.paginator.num_pages
        # return Response(OrderedDict([
        #     ('count', self.page.paginator.count),
        #     ('next', self.get_next_link()),
        #     ('previous', self.get_previous_link()),
        #     ('results', data),
        #     ('current_page_num', current_page_num),
        #     ('total_pages', total_pages)
        # ]))