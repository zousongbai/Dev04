
from django.http import JsonResponse,Http404
from projects.models import Projects
from .serializers import ProjectsSerializer,ProjectsModelSerializer

from rest_framework.response import Response
from rest_framework import status # 自定义状态码需导入status
from rest_framework.generics import GenericAPIView
# （3）步骤三：导入DjangoFilterBackend过滤引擎
from django_filters.rest_framework import DjangoFilterBackend # 导入DjangoFilterBackend过滤的引擎

class ProjectsView(GenericAPIView):

    queryset =Projects.objects.all()
    serializer_class = ProjectsModelSerializer

    # （1）步骤一：安装：django - filter第三方模块　
    # （2）步骤二：进行注册子应用操作：因为django - filter是第三方的子应用，所以需要在全局Dev04 / settings.py文件中指定过滤引擎。
    # （4）步骤四：filter_backends来指定使用的过滤的引擎，如果有多个过滤引擎，可以在列表中添加

    # 也可以在全局settings.py配置文件中指定所用视图公用的过滤引擎
    # 如果视图中未指定，那么会使用全局的过滤引擎；如果视图中有指定，那么会使用视图中指定的过滤引擎（优先级更高）
    # filter_backends = [DjangoFilterBackend]
    # （5）步骤五：filterset_fields来指定需要过滤的字段，字段名称一定要与模型类中的字段名称保持一致，并且为精确匹配。
    filterset_fields=['name','leader','id']

    def get(self, request):  # request:需要request接收，接收http的request对象
        """获取项目的所有信息"""

        # （6）步骤六：需要调用.filter_queryset()方法，需要传递一个查询集对象，并返回一个查询集
        projects_object=self.get_queryset()

        # 过滤：将需要过滤的查询集传给filter_queryset
        projects_object=self.filter_queryset(projects_object)

        # name=request.query_params.get('name')
        # if name is not None:
        #     # 如果不为空，则在查询集上调用filter,查询出来的也是查询集，则覆盖之前的查询集
        #     projects_object=projects_object.filter(name=name)

        serializer_obj = self.get_serializer(instance=projects_object, many=True) # 使用父类提供的get_serializer()方法

        return Response(serializer_obj.data,status=status.HTTP_200_OK)
        #  自定义状态码：status.HTTP_200_OK

    def post(self, request):
        """创建项目"""
        # ret不能放在全局，因为其他接口请求的时候，会状态的更新，所以不能放在全局
        ret = {
            "msg": "",
            "code": 0
        }

        # serializer_obj1 = ProjectsModelSerializer(data=request.data) # 根据请求头的Content-Type，就会自动的解析
        serializer_obj1 = self.get_serializer(data=request.data)
        try:
            # raise_exception=True：当校验失败，会报异常
            serializer_obj1.is_valid(raise_exception=True)
        except Exception as e:
            ret['msg'] = '参数有误'
            ret.update(serializer_obj1.errors)
            # return JsonResponse(ret, status=400)
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)

        # 在序列化器对象调用save方法时，传递的关键字参数，会自动添加到序列化器类中的create方法，validated_data字典中
        # serializer_obj1.save(user='小狼')
        serializer_obj1.save()

        # （4）步骤四：向前端返回json格式的数据
        ret['msg'] = '成功'
        ret.update(serializer_obj1.data)
        # return JsonResponse(ret, status=201)
        return Response(ret,status=status.HTTP_201_CREATED)

class ProjectDetailView(GenericAPIView):
    def get_object(self, pk):
        """获取模型类对象"""
        try:
            # 获取模型类对象
            obj = Projects.objects.get(id=pk)
        except Exception as e:
            result = {
                "msg": "参数有误",
                "code": 0
            }
            # return JsonResponse(result, status=400)
            # 抛出异常
            raise Http404
        return obj

    def get(self, request, pk):
        """获取项目详情"""

        # 获取模型类对象
        obj=self.get_object(pk)

        # serializer_obj = ProjectsModelSerializer(instance=obj)  # instance：可以接收模型类对象，也可以接收查询集对象。返回单个数据是，此处是模型类对象
        serializer_obj = self.get_serializer(instance=obj)

        return Response(serializer_obj.data,status=status.HTTP_200_OK)

    def put(self, request, pk):
        """更新项目"""

        # ret不能放在全局，因为其他接口请求的时候，会状态的更新，所以不能放在全局
        ret = {
            "msg": "",
            "code": 0
        }

        # 获取模型类对象
        obj = self.get_object(pk)

        # serializer_obj1 = ProjectsModelSerializer(instance=obj,data=request.data)
        serializer_obj1 = self.get_serializer(instance=obj, data=request.data)
        # data：做数据校验的工作，即反列化。涉及到数据校验，就需要给data传参
        # instance：做的是序列化操作
        # 同时给data和instance传参，往往做的是创建，意思是对obj对象进行修改，前端传的参数用data接收，更新的对象用instance去指定


        try:
            # raise_exception=True：当校验失败，会报异常
            # ②序列化器对象调用is_valid方法去做校验
            serializer_obj1.is_valid(raise_exception=True)
        except Exception as e:
            # ③校验之后，如果有异常，就处理异常后，再返回
            ret['msg'] = '参数有误'
            ret.update(serializer_obj1.errors)
            # return JsonResponse(ret, status=400)
            return Response(ret,status=status.HTTP_400_BAD_REQUEST)

        # 调用序列化器对象中的save方法
        # serializer_obj1.save(user='花花')
        serializer_obj1.save()

        # 使用序列化器对象.data返回
        # return JsonResponse(serializer_obj1.data, status=201)
        return Response(serializer_obj1.data,status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """删除项目"""
        # 获取模型类对象
        obj = self.get_object(pk)

        # 删除
        obj.delete()

        # 返回
        python_data = {
            'msg': '删除成功',
            'code': 1
        }
        # return JsonResponse(python_data, status=200)
        return Response(python_data,status=status.HTTP_204_NO_CONTENT)
