import json
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Testcases
from . import serializers
from testcases.models import Testcases
from utils import handle_data


class TestcasesViewSet(ModelViewSet):
    """
    list:
    返回接口（多个）列表数据

    create:
    创建接口

    retrieve:
    返回接口（单个）详情数据

    update:
    更新（全）接口

    partial_update:
    更新（部分）接口

    destroy:
    删除接口

    testcases:
    返回某个接口的所有用例信息（ID和名称）

    configures:
    返回某个接口的所有配置信息（ID和名称）
    """
    queryset = Testcases.objects.all()
    serializer_class = serializers.TestcasesModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ('id', 'name')

    def retrieve(self, request, *args, **kwargs):
        """重写retrieve"""
        # 获取用例信息
        testcase_obj = self.get_object()
        # 获取用例前置信息
        testcase_include = json.loads(testcase_obj.include, encoding='utf-8')
        # 获取用例请求信息
        testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
        # 获取接口的请求信息：先获取最外层test，再获取request
        testcase_request_data = testcase_request.get('test').get('request')

        # 处理validate参数：先获取最外层test，再获取validate
        # 后端从数据库读取的类型：[{"check":"status_code","expected":200,"comparator":"equals"}]
        # 前端需要的类型：[{"key": "status_code", "value": 200, "comparator": 'equals', "param_type": 'int'}]
        testcase_validate = testcase_request.get('test').get('validate')
        # 将后端的类型转换为前端需要的类型
        testcase_validate_list = handle_data.handle_data1(testcase_validate)
