
from django.http import JsonResponse,Http404
from projects.models import Projects
from .serializers import ProjectsSerializer,ProjectsModelSerializer

from rest_framework.response import Response
from rest_framework import status # 自定义状态码需导入status
from rest_framework.generics import GenericAPIView
# （3）步骤三：导入DjangoFilterBackend过滤引擎
from django_filters.rest_framework import DjangoFilterBackend # 导入DjangoFilterBackend过滤的引擎
from rest_framework.filters import OrderingFilter
# 导入自定义的分页引擎，用于仅仅指定对某个视图来进行分页
from utils.pagination import MyPagination

class ProjectsView(GenericAPIView):

    queryset =Projects.objects.all()
    serializer_class = ProjectsModelSerializer

    # （1）步骤一：安装：django - filter第三方模块　
    # （2）步骤二：进行注册子应用操作：因为django - filter是第三方的子应用，所以需要在全局Dev04 / settings.py文件中指定过滤引擎。
    # （4）步骤四：filter_backends来指定使用的过滤的引擎，如果有多个过滤引擎，可以在列表中添加

    # 也可以在全局settings.py配置文件中指定所用视图公用的过滤引擎
    # 如果视图中未指定，那么会使用全局的过滤引擎；如果视图中有指定，那么会使用视图中指定的过滤引擎（优先级更高）
    # filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filter_backends = [DjangoFilterBackend, OrderingFilter] # 指定排序引擎
    # （5）步骤五：filterset_fields来指定需要过滤的字段，字段名称一定要与模型类中的字段名称保持一致，并且为精确匹配。
    filterset_fields=['name','leader','id']
    # 指定哪些字段排序
    ordering_fields=['id','name']
    # 备注：先对id进行升序排序，然后对于name进行升序排序

    # 在视图中指定分页引擎类，仅仅指定对某个视图来进行分页　
    pagination_class = MyPagination

    def get(self, request):  # request:需要request接收，接收http的request对象
        """获取项目的所有信息"""
        # projects_object=self.get_queryset()
        # 过滤：将需要过滤的查询集传给filter_queryset
        # projects_object=self.filter_queryset(projects_object)
        projects_object = self.filter_queryset(self.get_queryset())

        # 分页功能使用父类的paginate_queryset
        page=self.paginate_queryset(projects_object)

        # 判断是否有分页引擎，没有则返回所有的数据
        if page is not None:
            # 如果page返回的不是空，说明指定了分页的引擎，需要进行分页
            # 先调用序列化器，得到序列化器对象
            serializer_obj=self.get_serializer(instance=page,many=True) # 因为分页返回的数据有多条，所以需要使用many=True
            # serializer_obj.data：使用的是序列化处理之后的数据，用data属性
            return self.get_paginated_response(serializer_obj.data)
        serializer_obj = self.get_serializer(instance=projects_object, many=True) # 使用父类提供的get_serializer()方法

        return Response(serializer_obj.data,status=status.HTTP_200_OK)
        #  自定义状态码：status.HTTP_200_OK

    def post(self, request):
        """创建项目"""

        # serializer_obj1 = ProjectsModelSerializer(data=request.data) # 根据请求头的Content-Type，就会自动的解析
        serializer_obj1 = self.get_serializer(data=request.data)

        serializer_obj1.is_valid(raise_exception=True)

        serializer_obj1.save()

        # 向前端返回json格式的数据
        return Response(serializer_obj1.data,status=status.HTTP_201_CREATED)

class ProjectDetailView(GenericAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer

    def get(self, request, pk):
        """获取项目详情"""

        # 获取模型类对象
        # obj=self.get_object(pk)
        obj = self.get_object()

        # serializer_obj = ProjectsModelSerializer(instance=obj)  # instance：可以接收模型类对象，也可以接收查询集对象。返回单个数据是，此处是模型类对象
        serializer_obj = self.get_serializer(instance=obj)

        return Response(serializer_obj.data,status=status.HTTP_200_OK)

    def put(self, request, pk):
        """更新项目"""

        # 获取模型类对象
        # obj = self.get_object(pk)
        obj = self.get_object()

        serializer_obj1 = self.get_serializer(instance=obj, data=request.data)
        # data：做数据校验的工作，即反列化。涉及到数据校验，就需要给data传参
        # instance：做的是序列化操作
        # 同时给data和instance传参，往往做的是创建，意思是对obj对象进行修改，前端传的参数用data接收，更新的对象用instance去指定

        # 在视图中抛出的异常，DRF会自动处理
        # 直接将报错信息以json格式返回
        serializer_obj1.is_valid(raise_exception=True)


        # 调用序列化器对象中的save方法
        # serializer_obj1.save(user='花花')
        serializer_obj1.save()

        # 使用序列化器对象.data返回
        return Response(serializer_obj1.data,status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """删除项目"""
        # 获取模型类对象
        # obj = self.get_object(pk)
        obj = self.get_object()

        # 删除
        obj.delete()

        return Response(None,status=status.HTTP_204_NO_CONTENT)
