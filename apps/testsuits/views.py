from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

# 导入查询集
from .models import Testsuits
# 导入序列化器类
from .serializers import TestsuitsModelSerializer
class TestsuitsViewSet(ModelViewSet):
    queryset = Testsuits.objects.all()
    serializer_class = TestsuitsModelSerializer
    # 指定认证
    permission_classes =[permissions.IsAuthenticated]
    # 指定排序字段
    ordering_fields=['id','name']
    # 获取环境变量的名称和id

    # # 重写get_serializer_class
    # def get_serializer_class(self):
    #     # if self.action=='names':
    #     #     return EnvsNamesSerializer
    #     # else:
    #     #     # 返回序列化器类
    #     #     return self.serializer_class
    #
    #     # 或下面三目写法
    #     return EnvsNamesSerializer if self.action == 'names' else  self.serializer_class


    # 重写retrieve
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {
            'name': instance.name,
            'project_id': instance.project_id,
            'include': instance.include
        }
        return Response(data)