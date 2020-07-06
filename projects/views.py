import json

from django.http import JsonResponse
from django.views import View
from projects.models import Projects
from .serializers import ProjectsSerializer

ret = {
    "msg": "",
    "code": 0
}


# 使用两个类视图：是因为有的接口需要传递id，有的接口不需要传递id，把传id的放在一个类似图中，不传id的放在另外一个类视图中
class ProjectsView(View):
    """
    一、需求：需要设置5个接口，来提供前端使用对项目的增删改查操作
    （1）需要能获取到项目的列表数据（获取多条项目的数据或者所有数据）
    ①url：/projects/
    ②method：GET
    ③response data：返回的数据json格式
    （3）能够创建项目（创建一个项目）
    ①url：/projects/
    ②method：POST
    ③request data：请求的数据json格式
    ④response data：返回的数据json格式 1）{msg:'创建成功',code:0}
    """

    def get(self, request):  # request:需要request接收，接收http的request对象
        """获取项目的所有信息"""
        # （1）步骤一：从数据库中获取所有的项目信息（返回的是查询集）
        projects_object = Projects.objects.all()
        # （2）步骤二：需要将模型类对象（查询集）转化为嵌套字典的列表

        # 创建序列化器对象
        serializer_obj = ProjectsSerializer(instance=projects_object, many=True)
        # 备注：
        # ①可以使用序列化器类来进行序列化输出
        # 1）instance：可以传模型类对象，
        # 2）instance：也可以传查询集对象（多条记录）。返回多个数据是，此处是查询集对象，由于返回多条数据，所以一定要加上many=True
        # ②可以ProjectsSerializer序列化器对象，调用data属性，可以将模型类对象转化为python中的数据类型
        # ③如果未传递many=True参数，那么序列化器对象.data，返回字典，否则返回一个嵌套字典的列表

        # （3）步骤三：向前端返回json格式的数据
        return JsonResponse(serializer_obj.data, safe=False, status=200)
        # 备注：列表必须加safe，字典可以不加safe

    def post(self, request):
        """创建项目"""
        # （1）步骤一：获取新的项目信息，并转化为python中的数据类型（字典或者嵌套字典的列表）
        # 因为：需要将前端传递的数据进行校验，或做数据保存，更加方便的获取到前端传递的数据，所以有必要转化为python当中的数据类型

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
        serializer_obj1 = ProjectsSerializer(data=python_data)
        try:
            # raise_exception=True：当校验失败，会报异常
            serializer_obj1.is_valid(raise_exception=True)
        except Exception as e:
            ret['msg'] = '参数有误'
            ret.update(serializer_obj1.errors)
            return JsonResponse(ret, status=400)

        # （3）步骤三：创建模型类对象
        # 将创建项目的逻辑放在序列化器类里面
        # 方法一：
        # obj = Projects.objects.create(**serializer_obj1.validated_data)

        # 方法二：
        # obj =Projects(**serializer_obj1.validated_data)
        # # 备注：validated_data：校验通过的数据
        # # 提交
        # obj.save()

        # 在序列化器对象调用save方法时，传递的关键字参数，会自动添加到序列化器类中的create方法，validated_data字典中
        # serializer_obj1.save(user='小狼')
        serializer_obj1.save()

        # （4）步骤四：向前端返回json格式的数据
        ret['msg'] = '成功'
        ret.update(serializer_obj1.data)
        return JsonResponse(ret, status=201)


class ProjectDetailView(View):
    """
    （2）需要能获取到项目的详情数据（获取前端指定的某一条数据）
   ①url：/projects/<int:pk>/
   ②method：GET
   ③response data：返回的数据json格式
   （4）能够更新项目（只更新某一个项目）
   ①url：/projects/<int:pk>/
   ②method：PUT
   ③request data：请求的数据json格式
   ④response data：返回的数据json格式
   （5）能够删除项目（只删除某一个项目）
   ①url：/projects/<int:pk>/
   ②method：DELETE
   ③request data：请求的数据json格式
   ④response data：返回的数据json格式 备注：URL相同的说明需要在同一个类视图下面创建不同的实例方法
    """

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
        serializer_obj = ProjectsSerializer(instance=obj)  # instance：可以接收模型类对象，也可以接收查询集对象。返回单个数据是，此处是模型类对象
        # ②获取数据：使用序列化器对象的data属性：serializer_obj.data

        # （3）步骤三：向前端返回json格式的数据
        return JsonResponse(serializer_obj.data)

    def put(self, request, pk):
        """更新项目"""
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

        # ①序列化器对象一：将转换之后的数据python_data，传给data，主要做校验
        # serializer_obj1 = ProjectsSerializer(data=python_data)

        # 如果在定义序列化器对象时，同时指定data和instance参数，有如下情况：
        # ①调用序列化器对象.save()，会自动调用序列化器类中的update方法
        serializer_obj1 = ProjectsSerializer(instance=obj,data=python_data)
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

        # ④如果没有异常，就去更新，更新的数据在obj里面
        # （3）步骤三：更新操作
        # 如果前端传空就更新，如果不为空则更新
        # ⑤用校验通过的数据（serializer_obj1.validated_data）去获取
        # obj.name = serializer_obj1.validated_data.get('name') or obj.name
        # obj.leader = serializer_obj1.validated_data.get('leader') or obj.leader
        # obj.tester = serializer_obj1.validated_data.get('tester') or obj.tester
        # obj.programmer = serializer_obj1.validated_data.get('programmer') or obj.programmer
        # obj.desc = serializer_obj1.validated_data.get('desc') or obj.desc
        # # 或
        # # Projects.objects.filter(id=pk).update(**python_data)
        #
        # # 保存
        # obj.save()

        # （4）步骤四：向前端返回json格式的数据
        # 序列化器对象二：给instance传参，主要做的是，将模型类对象返回给前端
        # serializer_obj = ProjectsSerializer(instance=obj)  # 序列化输出时，使用这行代码

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

# summary：
# （1）上述5个接口的实现步骤
# ①数据校验
# ②将请求消息（json格式的字符串）转化为模型类对象（python中数据类型）
# 1）这个过程叫反序列化
# 2）往往为json格式的字符串(xml）
# ③数据库操作（创建、更新、获取、删除）
# ④将模型类对象转换为响应数据（json格式的字符串）返回
# 1）这个过程叫序列化
# 2）往往为json格式的字符串（xml）

# （2）5个接口中有哪些痛点
# ①代码冗余非常大
# ②数据校验非常麻烦
# ③获取列表数据：没有分页操作、过滤操作、没有排序操作
# ④不支持以表单来提交参数
# ⑤无法自动生成接口文档
#
