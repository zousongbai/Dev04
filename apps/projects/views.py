import logging
from rest_framework.response import Response
# 导入视图集
from rest_framework import viewsets
# 导入action装饰器
from rest_framework.decorators import action
from projects.models import Projects
from interfaces.models import Interfaces
from django.db.models import Count
from rest_framework import permissions

from .serializers import (ProjectsModelSerializer,
                          ProjectsNameModelSerializer,
                          InterfacesByProjectsIdModelSerializer1,
                         )
# 定义日志器：此处的名称要与全局日志器的日志保持一致
# 定义日志器用于记录日志，logging.getLogger('全局配置setting.py中定义的日志器')
logger=logging.getLogger('mytest')


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
    permission_classes = [permissions.IsAuthenticated] # IsAuthenticated：必须登录才能访问

    def list(self, request, *args, **kwargs):
        # 继承父类的list()方法
        response=super().list(request, *args, **kwargs)
        # 改造的数据在data字典的results键中
        results=response.data['results']
        for item in results:
            # item为一条项目数据所在的字典
            # 需要获取当前项目所属的接口总数、用例总数、配置总数、套件总数
            # 项目id
            project_id = item.get('id')
            # # 接口总数
            # interface_count = Interfaces.objects.filter(project_id=project_id).count()
            # # 接口信息
            # interface_qs = Interfaces.objects.filter(project_id=project_id)
            # # 项目所属接口所属所有用例总数
            # for obj in interface_qs:
            #     # 接口id
            #     interface_id = obj.id
            #     # 当前项目的用例总数
            #     TestCase.ojbects.filter(interface_id=interface_id).count()

            # a.使用.annotate()方法，那么会自动使用当前模型类的主键作为分组条件
            # b.使用.annotate()方法里可以添加聚合函数，计算的名称为一般从表模型类名小写（还需要在外键字段上设置related_name）
            # c.values可以指定需要查询的字段（默认为所用字段）
            # d.可以给聚合函数指定别名，默认为testcases__count

            interfaces_obj = Interfaces.objects.annotate(testcases=Count('testcases')).values('id', 'testcases'). \
                filter(project_id=project_id)
            # 备注：
            # Interfaces.objects.annotate：对当前接口表id进行分组
            # Count('testcases')：计算所属接口的用例总数
            # values('id', 'testcases')：返回当前的接口id、testcases

            Interfaces.objects.annotate(Count('testcases'))

    @action(methods=['get'],detail=False)
    def names(self,request,*args,**kwargs):
        """获取项目名称"""
        # 不对name进行分页
        # 调用父类list的方法
        return self.list(request,*args,**kwargs)

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

        serializer_obj =self.get_serializer(instance=instance)
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

