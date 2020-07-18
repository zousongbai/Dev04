from projects.models import Projects
from .serializers import ProjectsModelSerializer
# 导入DjangoFilterBackend过滤引擎
from django_filters.rest_framework import DjangoFilterBackend  # 导入DjangoFilterBackend过滤的引擎
from rest_framework.filters import OrderingFilter
from rest_framework import mixins
# 导入通用的扩展类
from rest_framework import generics
from rest_framework.generics import GenericAPIView
# 导入视图集
from rest_framework import viewsets


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

    # 备注：先对id进行升序排序，然后对于name进行升序排序

    def destroy(self, request, *args, **kwargs):
        """父类删除后返回空，重写destroy方法删除后返回一个特定字符"""
