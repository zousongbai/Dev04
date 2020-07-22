import logging
from rest_framework.response import Response
from projects.models import Projects
# 导入DjangoFilterBackend过滤引擎
from django_filters.rest_framework import DjangoFilterBackend  # 导入DjangoFilterBackend过滤的引擎
from rest_framework.filters import OrderingFilter
from rest_framework import mixins
# 导入通用的扩展类
from rest_framework import generics
from rest_framework.generics import GenericAPIView
# 导入视图集
from rest_framework import viewsets
from interfaces.models import Interfaces
# 导入action装饰器
from rest_framework.decorators import action
from .serializers import (ProjectsModelSerializer,
                          ProjectsNameModelSerializer,
                          InterfacesByProjectsIdModelSerializer,
                          InterfacesByProjectsIdModelSerializer1,
                         )
# 定义日志器：此处的名称要与全局日志器的日志保持一致
# 定义日志器用于记录日志，logging.getLogger('全局配置setting.py中定义的日志器')
logger=logging.getLogger('mytest')

class ProjectsView(generics.ListCreateAPIView):
    # 继承的时候，一定要先继承mixins扩展类，再继承GenericAPIView
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer

    # 指定过滤引擎、排序引擎
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_fields来指定需要过滤的字段，字段名称一定要与模型类中的字段名称保持一致，并且为精确匹配。
    filterset_fields = ['name', 'leader', 'id']
    # 指定哪些字段排序
    ordering_fields = ['id', 'name']
    # 备注：先对id进行升序排序，然后对于name进行升序排序


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer


# 合并上面两个类：ProjectsView、ProjectDetailView

# 使用ModelViewSet类对上面提供的五个方法进行优化：class ProjectsViewSet(viewsets.ModelViewSet):
# 如果仅仅是读取数据，则继承ReadOnlyModelViewSet类：class ProjectsViewSet(viewsets.ReadOnlyModelViewSet):
class ProjectsViewSet(viewsets.ModelViewSet):
    """
    list:
        获取项目的列表信息
    retrive:
        获取项目详情数据
    create:
        创建项目
    names:
        获取项目名称
    interfaces:
        获取某个项目下的接口名称
    update:
        更新项目
    delete:
        删除项目
    partial_update:
        部分更新
    read:
        获取项目详情
    """

    # 继承的时候，一定要先继承mixins扩展类，再继承GenericAPIView
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer

    # # 指定过滤引擎、排序引擎
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # # filterset_fields来指定需要过滤的字段，字段名称一定要与模型类中的字段名称保持一致，并且为精确匹配。
    # # filterset_fields = ['name', 'leader', 'id']
    # # 指定哪些字段排序
    # ordering_fields = ['id', 'name']

    # （1）可以使用action装饰器去自定义动作方法（action）
    # （2）methods参数默认为['get']，可以定义支持请求方式['get', 'post', 'put']
    # （3）detail参数为必传参数，指定是否为详情数据。
    # ①如果需要传递主键id，那么detail = True
    # ②否则detail = False
    # （4）url_path：指定url路径部分，默认为action名称（当前为names）
    # （5）url_name：指定url的名称，默认为action名称（当前为names，完整的路由名称为action名称(name),然后跟上list或其他），会在前后端不分离的时候用到
    @action(methods=['get'],detail=False)
    def names(self,request):
        """获取项目名称"""
        # 进行过滤和分页操作
        # ①过滤
        qs=self.filter_queryset(self.get_queryset())
        # ②分页
        # page=self.paginate_queryset(qs)
        # 判断是否有分页引擎，没有则返回所有的数据
        # if page is not None:
        #     # 先调用序列化器，得到序列化器对象
        #     serializer_obj = self.get_serializer(instance=page, many=True)
        #     # 备注：因为分页返回的数据有多条，所以需要使用many=True
        #     return self.get_paginated_response(serializer_obj.data)

        # # 使用序列化器，得到序列化器对象
        # serializer_obj=ProjectsNameModelSerializer(instance=self.get_queryset(),many=True)
        # # 备注：因为项目名称有多个，所以需要传many=True
        # serializer_obj = self.get_serializer(instance=self.get_queryset(), many=True)
        serializer_obj = self.get_serializer(instance=qs, many=True)

        data=serializer_obj.data
        # 记录调试的日志
        logger.debug(data)
        return Response(data)

    @action(detail=True )
    # 默认methods=['get']
    # 如果需要传递主键id，那么detail = True
    def interfaces(self,request,*args,**kwargs):
        # 获取当前的模型类对象
        instance=self.get_object()
        # 进行过滤和分页操作
        # ①过滤
        # qs = self.filter_queryset(self.get_queryset())
        qs=Interfaces.objects.filter(projects=instance)
        # ②分页
        page = self.paginate_queryset(qs)
        # 判断是否有分页引擎，没有则返回所有的数据
        if page is not None:
            # 先调用序列化器，得到序列化器对象
            serializer_obj = self.get_serializer(instance=page, many=True)
            # 备注：因为分页返回的数据有多条，所以需要使用many=True
            return self.get_paginated_response(serializer_obj.data)
        serializer_obj =self.get_serializer(instance=qs)
        return Response(serializer_obj.data)

    def get_serializer_class(self):
        """重写get_serializer_class"""
        # 使用self.get_serializer的时候胡调用get_serializer_class
        if self.action=='names':
            # self.action：获取当前的action
            return ProjectsNameModelSerializer
        elif self.action=='interfaces':
            # return InterfacesByProjectsIdModelSerializer
            return InterfacesByProjectsIdModelSerializer1
        else:
            return self.serializer_class

