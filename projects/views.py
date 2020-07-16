from django.http import JsonResponse, Http404
from projects.models import Projects
from .serializers import ProjectsSerializer, ProjectsModelSerializer
from rest_framework.response import Response
from rest_framework import status  # 自定义状态码需导入status
from rest_framework.generics import GenericAPIView
# （3）步骤三：导入DjangoFilterBackend过滤引擎
from django_filters.rest_framework import DjangoFilterBackend  # 导入DjangoFilterBackend过滤的引擎
from rest_framework.filters import OrderingFilter
# 导入自定义的分页引擎，用于仅仅指定对某个视图来进行分页
from utils.pagination import MyPagination
from rest_framework import mixins
# （1）可以先继承DRF中的mixins扩展类
# （2）然后再继承GenericAPIView
# 因为源码中使用了get_object()，又因为get_object()只有GenericAPIView才有，所以一定要先继承mixins扩展类，再继承GenericAPIView
# （3）ListModelMixin->.list()方法：实现获取列表数据
# （4）CreateModelMixin->.create()方法：实现创建数据
class ProjectsView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   GenericAPIView
                   ):
    # 继承的时候，一定要先继承mixins扩展类，再继承GenericAPIView
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer

    # （1）步骤一：安装：django - filter第三方模块　
    # （2）步骤二：进行注册子应用操作：因为django - filter是第三方的子应用，所以需要在全局Dev04 / settings.py文件中指定过滤引擎。
    # （4）步骤四：filter_backends来指定使用的过滤的引擎，如果有多个过滤引擎，可以在列表中添加

    # 也可以在全局settings.py配置文件中指定所用视图公用的过滤引擎
    # 如果视图中未指定，那么会使用全局的过滤引擎；如果视图中有指定，那么会使用视图中指定的过滤引擎（优先级更高）
    # filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # 指定排序引擎
    # （5）步骤五：filterset_fields来指定需要过滤的字段，字段名称一定要与模型类中的字段名称保持一致，并且为精确匹配。
    filterset_fields = ['name', 'leader', 'id']
    # 指定哪些字段排序
    ordering_fields = ['id', 'name']
    # 备注：先对id进行升序排序，然后对于name进行升序排序

    # 在视图中指定分页引擎类，仅仅指定对某个视图来进行分页　
    pagination_class = MyPagination

    def get(self, request, *args, **kwargs):  # request:需要request接收，接收http的request对象
        """获取项目的所有信息"""
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """创建项目"""

        # serializer_obj1 = self.get_serializer(data=request.data)
        #
        # serializer_obj1.is_valid(raise_exception=True)
        #
        # serializer_obj1.save()
        #
        # # 向前端返回json格式的数据
        # return Response(serializer_obj1.data,status=status.HTTP_201_CREATED)

        return self.create(request, *args, **kwargs)


class ProjectDetailView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        GenericAPIView
                        ):
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer

    def get(self, request, *args, **kwargs):  # pk会传给**kwargs
        """获取项目详情"""

        # 获取模型类对象
        # obj = self.get_object()
        #
        # serializer_obj = self.get_serializer(instance=obj)
        #
        # return Response(serializer_obj.data,status=status.HTTP_200_OK)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """更新项目"""

        # 获取模型类对象
        # obj = self.get_object()
        #
        # serializer_obj1 = self.get_serializer(instance=obj, data=request.data)

        # # 在视图中抛出的异常，DRF会自动处理
        # # 直接将报错信息以json格式返回
        # serializer_obj1.is_valid(raise_exception=True)

        # serializer_obj1.save()
        #
        # # 使用序列化器对象.data返回
        # return Response(serializer_obj1.data,status=status.HTTP_201_CREATED)

        #  父类提供的update()方法，既支持全部更新也支持部分更新
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """删除项目"""
        # 获取模型类对象
        # obj = self.get_object()
        #
        # # 删除
        # obj.delete()
        #
        # return Response(None,status=status.HTTP_204_NO_CONTENT)
        return self.destroy(request, *args, **kwargs)
