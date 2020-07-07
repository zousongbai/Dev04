import json

from django.http import JsonResponse
from django.views import View
from projects.models import Projects
from .serializers import ProjectsSerializer,ProjectsModelSerializer


class ProjectsView(View):

    def get(self, request):  # request:需要request接收，接收http的request对象
        """获取项目的所有信息"""
        # （1）步骤一：从数据库中获取所有的项目信息（返回的是查询集）
        projects_object = Projects.objects.all()

        # （2）步骤二：需要将模型类对象（查询集）转化为嵌套字典的列表

        # 创建序列化器对象
        serializer_obj = ProjectsModelSerializer(instance=projects_object, many=True)

        # （3）步骤三：向前端返回json格式的数据
        return JsonResponse(serializer_obj.data, safe=False, status=200)
        # 备注：列表必须加safe，字典可以不加safe

    def post(self, request):
        """创建项目"""
        # （1）步骤一：获取新的项目信息，并转化为python中的数据类型（字典或者嵌套字典的列表）
        # 因为：需要将前端传递的数据进行校验，或做数据保存，更加方便的获取到前端传递的数据，所以有必要转化为python当中的数据类型

        # ret不能放在全局，因为其他接口请求的时候，会状态的更新，所以不能放在全局
        ret = {
            "msg": "",
            "code": 0
        }
        # 请求数据
        request_data = request.body  # json格式数据往往存放在body里面

        try:
            # 请求体的数据，转化成python中的数据类型（字典或者嵌套字典的列表）
            python_data = json.loads(request_data)
        except Exception as e:
            # 不是json则报错，并返回结果
            result = {
                'msg': '参数有误',
                'code': 0
            }
            return JsonResponse(result, status=400)

        # （2）步骤二：校验传递的数据是否正确（非常复杂）

        # 在定义序列化器对象时，只给data传参
        # ①使用序列化器对象.save()方法，会自动调用序列化器类中的create()方法
        serializer_obj1 = ProjectsModelSerializer(data=python_data)
        try:
            # raise_exception=True：当校验失败，会报异常
            serializer_obj1.is_valid(raise_exception=True)
        except Exception as e:
            ret['msg'] = '参数有误'
            ret.update(serializer_obj1.errors)
            return JsonResponse(ret, status=400)

        # 在序列化器对象调用save方法时，传递的关键字参数，会自动添加到序列化器类中的create方法，validated_data字典中
        # serializer_obj1.save(user='小狼')
        serializer_obj1.save()

        # （4）步骤四：向前端返回json格式的数据
        ret['msg'] = '成功'
        ret.update(serializer_obj1.data)
        return JsonResponse(ret, status=201)


class ProjectDetailView(View):

    def get(self, request, pk):
        """获取项目详情"""
        # （1）步骤一：校验参数，校验参数pk是否存在
        try:
            obj = Projects.objects.get(id=pk)  # get：结果没有或返回多条结果都会报错
        except Exception as e:
            result = {
                'msg': '参数有误',
                'code': 0
            }
            return JsonResponse(result, status=400)

        # （2）步骤二：从数据库中获取模型类对象数据
        # ①进行序列化输出，需要创建序列化器类对象
        serializer_obj = ProjectsModelSerializer(instance=obj)  # instance：可以接收模型类对象，也可以接收查询集对象。返回单个数据是，此处是模型类对象
        # ②获取数据：使用序列化器对象的data属性：serializer_obj.data

        # （3）步骤三：向前端返回json格式的数据
        return JsonResponse(serializer_obj.data)

    def put(self, request, pk):
        """更新项目"""

        # ret不能放在全局，因为其他接口请求的时候，会状态的更新，所以不能放在全局
        ret = {
            "msg": "",
            "code": 0
        }

        # （1）步骤一：校验pk值否存在，并获取待更新的模型类对象
        try:
            obj = Projects.objects.get(id=pk)  # get：结果没有或返回多条结果都会报错
        except Exception as e:
            result = {
                'msg': '参数有误',
                'code': 0
            }
            return JsonResponse(result, status=400)

        # （2）步骤二：获取新的项目信息并校验
        request_data = request.body  # json格式数据往往存放在body里面

        try:
            # 请求体的数据，转化成python中的数据类型（字典或者嵌套字典的列表）
            python_data = json.loads(request_data)
        except Exception as e:
            # 不是json则报错，并返回结果
            result = {
                'msg': '参数有误',
                'code': 0
            }
            return JsonResponse(result, status=400)

        # 如果在定义序列化器对象时，同时指定data和instance参数，有如下情况：
        # ①调用序列化器对象.save()，会自动调用序列化器类中的update方法
        serializer_obj1 = ProjectsModelSerializer(instance=obj,data=python_data)
        # data：做数据校验的工作，即反列化
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
            return JsonResponse(ret, status=400)

        # 调用序列化器对象中的save方法
        # serializer_obj1.save(user='花花')
        serializer_obj1.save()

        # 使用序列化器对象.data返回
        return JsonResponse(serializer_obj1.data, status=201)

    def delete(self, request, pk):
        """删除项目"""
        # （1）步骤一：校验pk值否存在，并获取待删除的模型类对象
        try:
            obj = Projects.objects.get(id=pk)  # get：结果没有或返回多条结果都会报错
        except Exception as e:
            result = {
                'msg': '参数有误',
                'code': 0
            }
            return JsonResponse(result, status=400)

        # 删除
        obj.delete()

        # 返回
        python_data = {
            'msg': '删除成功',
            'code': 1
        }
        return JsonResponse(python_data, status=200)

