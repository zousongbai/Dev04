import json

from django.http import JsonResponse,Http404
from django.views import View
from projects.models import Projects
from interfaces.models import Interfaces
from .serializers import ProjectsSerializer,ProjectsModelSerializer
from interfaces.serializers import InterfacesModelSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status # 自定义状态码需导入status


# （1）步骤一：需要继承APIView
# ①对Django中的View进行了扩展
# ②具备认证、授权、限流、不同请求数据的解析
class ProjectsView(APIView):

    def get(self, request):  # request:需要request接收，接收http的request对象
        """获取项目的所有信息"""

        # （1）步骤一：从数据库中获取所有的项目信息（返回的是查询集）
        projects_object = Projects.objects.all()

        # （2）步骤二：需要将模型类对象（查询集）转化为嵌套字典的列表

        # 创建序列化器对象
        serializer_obj = ProjectsModelSerializer(instance=projects_object, many=True)

        # （3）步骤三：向前端返回json格式的数据
        # return JsonResponse(serializer_obj.data, safe=False, status=200)
        # 备注：列表必须加safe，字典可以不加safe

        # （2）步骤二：需要使用DRF中的Response去返回
        # ①对Django中的HttpResponse进行扩展
        # ②实现了根据请求头中Accept参数来动态返回
        # ③默认情况下，如果不传Accept参数或者传application / json，那么会返回json格式的数据
        # ④如果Accept参数为text / html，那么会返回可浏览的api页面（HTML页面）
        # ⑤Response第一个参数为：经过序列化之后的数据（往往需要使用序列化器对象.data）
        # ⑥status为指定响应状态码，不传默认200
        return Response(serializer_obj.data,status=status.HTTP_200_OK)
        #  自定义状态码：status.HTTP_200_OK

    def post(self, request):
        """创建项目"""
        # 继承APIView之后，request为Request
        # ①对Django中的HttpRequest进行了扩展
        # ②统一使用Request对象.data属性去获取json格式的参数，form表单参数、FILES
        # ③Django支持的参数获取方式，DRF都支持
        # ④.GET-->查询字符串参数-->.query_params
        # ⑤.POST-->x-www-form-urlencoded
        # ⑥.body-->获取请求体参数
        # ⑦Request对象.data属性为将请求数据转化为python中的字典（嵌套字典的列表）

        # ret不能放在全局，因为其他接口请求的时候，会状态的更新，所以不能放在全局
        ret = {
            "msg": "",
            "code": 0
        }
        # 请求数据
        # request_data = request.body  # json格式数据往往存放在body里面
        #
        # try:
        #     # 请求体的数据，转化成python中的数据类型（字典或者嵌套字典的列表）
        #     python_data = json.loads(request_data)
        # except Exception as e:
        #     # 不是json则报错，并返回结果
        #     result = {
        #         'msg': '参数有误',
        #         'code': 0
        #     }
        #     # return JsonResponse(result, status=400)
        #     return Response(result,status=status.HTTP_400_BAD_REQUEST)



        # （2）步骤二：校验传递的数据是否正确（非常复杂）

        # 在定义序列化器对象时，只给data传参
        # ①使用序列化器对象.save()方法，会自动调用序列化器类中的create()方法
        serializer_obj1 = ProjectsModelSerializer(data=request.data) # 根据请求头的Content-Type，就会自动的解析
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

class ProjectDetailView(APIView):
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

        # （2）步骤二：从数据库中获取模型类对象数据
        # ①进行序列化输出，需要创建序列化器类对象
        serializer_obj = ProjectsModelSerializer(instance=obj)  # instance：可以接收模型类对象，也可以接收查询集对象。返回单个数据是，此处是模型类对象
        # ②获取数据：使用序列化器对象的data属性：serializer_obj.data

        # （3）步骤三：向前端返回json格式的数据
        # return JsonResponse(serializer_obj.data)
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


        # 如果在定义序列化器对象时，同时指定data和instance参数，有如下情况：
        # ①调用序列化器对象.save()，会自动调用序列化器类中的update方法
        serializer_obj1 = ProjectsModelSerializer(instance=obj,data=request.data)
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
