from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

# 导入查询集
from .models import Envs
# 导入序列化器类
from .serializers import EnvsModelSerializer,EnvsNamesSerializer
class EnvsViewSet(ModelViewSet):
    # 查询集
    queryset = Envs.objects.all()
    # 序列化器类
    serializer_class = EnvsModelSerializer
    # 指定认证
    permission_classes =[permissions.IsAuthenticated]
    # 指定排序字段
    ordering_fields=['id','name']
    # 获取环境变量的名称和id

    # detail如果要传外键id，则设为True；不传外键id，则设为False
    @action(detail=False)
    def names(self,request, *args, **kwargs):
        # 获取查询集
        qs=self.get_queryset()
        return Response(self.get_serializer(qs,many=True).data)
        # 备注：因为有多个结果，所以需要设置many=True

    # 重写get_serializer_class
    def get_serializer_class(self):
        # if self.action=='names':
        #     return EnvsNamesSerializer
        # else:
        #     # 返回序列化器类
        #     return self.serializer_class

        # 或下面三目写法
        return EnvsNamesSerializer if self.action == 'names' else  self.serializer_class
