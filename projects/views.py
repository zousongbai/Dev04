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
# 导入action装饰器
from rest_framework.decorators import action
from .serializers import ProjectsModelSerializer,ProjectsNameModelSerializer

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
# GenericAPIView和APIView只支持对get、post、put、delete、patch等请求方法
# 如果要支持action（get、post、put、delete、patch等请求方法），那么需要继承ViewSet
# 当前ViewSet，无法支持.get_object()、.filter_queryset()、paginate_queryset()
# class ProjectsViewSet(viewsets.ViewSet):
# GenericViewSet才支持对列表数据进行过滤、排序、分页操作
# class ProjectsViewSet(mixins.ListModelMixin, # 提供list方法
#                       mixins.CreateModelMixin, # 提供create方法
#                       mixins.RetrieveModelMixin, # 提供retrieve方法
#                       mixins.UpdateModelMixin, # 提供update方法
#                       mixins.DestroyModelMixin, # 提供destroy方法
#                       viewsets.GenericViewSet):

# 使用ModelViewSet类对上面提供的五个方法进行优化：class ProjectsViewSet(viewsets.ModelViewSet):
# 如果仅仅是读取数据，则继承ReadOnlyModelViewSet类：class ProjectsViewSet(viewsets.ReadOnlyModelViewSet):
class ProjectsViewSet(viewsets.ModelViewSet):
    # 继承的时候，一定要先继承mixins扩展类，再继承GenericAPIView
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer

    # 指定过滤引擎、排序引擎
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_fields来指定需要过滤的字段，字段名称一定要与模型类中的字段名称保持一致，并且为精确匹配。
    filterset_fields = ['name', 'leader', 'id']
    # 指定哪些字段排序
    ordering_fields = ['id', 'name']

    # （1）可以使用action装饰器去自定义动作方法（action）
    # （2）methods参数默认为['get']，可以定义支持请求方式['get', 'post', 'put']
    # （3）detail参数为必传参数，指定是否为详情数据。
    # ①如果需要传递主键id，那么detail = True
    # ②否则detail = False
    # （4）url_path：指定url部分，默认为action名称（当前为names）
    # （5）url_name：指定url的名称，默认为action名称（当前为names）
    @action(methods=['get'],detail=False,)
    def names(self,request):
        """获取项目名称"""
        # 进行过滤和分页操作
        # ①过滤
        qs=self.filter_queryset(self.get_queryset())
        # ②分页
        page=self.paginate_queryset(qs)
        # 判断是否有分页引擎，没有则返回所有的数据
        if page is not None:
            # 先调用序列化器，得到序列化器对象
            serializer_obj = self.get_serializer(instance=page, many=True)
            # 备注：因为分页返回的数据有多条，所以需要使用many=True
            return self.get_paginated_response(serializer_obj.data)

        # # 使用序列化器，得到序列化器对象
        # serializer_obj=ProjectsNameModelSerializer(instance=self.get_queryset(),many=True)
        # # 备注：因为项目名称有多个，所以需要传many=True
        # serializer_obj = self.get_serializer(instance=self.get_queryset(), many=True)
        serializer_obj = self.get_serializer(instance=qs, many=True)

        return Response(serializer_obj.data)

    def get_serializer_class(self):
        """重写get_serializer_class"""
        # 使用self.get_serializer的时候胡调用get_serializer_class
        if self.action=='names':
            # self.action：获取当前的action
            return ProjectsNameModelSerializer
        else:
            return self.serializer_class