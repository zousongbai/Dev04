import json

from django.http import JsonResponse
from django.views import View
from projects.models import Projects


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
        python_data = []  # 嵌套字典的列表
        python_dict = {}
        for obj in projects_object:
            one_dict = {
                'id': obj.id,
                'name': obj.name,
                'leader': obj.leader,
            }
            # 把所有的数据放在列表里面
            python_data.append(one_dict)
        python_dict['msg'] = '获取数据成功'
        python_dict['code'] = 1
        # 将列表作为值
        python_dict['data'] = python_data

        # （3）步骤三：向前端返回json格式的数据
        return JsonResponse(python_dict, safe=False, status=200)
        # 备注：列表必须加safe，列表可以不加safe

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
        if ('name' not in python_data) or ('leader' not in python_data):
            #  判断name或leader不在python_data中，则报错误
            result = {
                'msg': '参数有误',
                'code': 0
            }
            return JsonResponse(result, status=400)

        # （3）步骤三：创建项目
        obj = Projects.objects.create(**python_data)

        # （4）步骤四：向前端返回json格式的数据
        python_dict = {
            'id': obj.id,
            'name': obj.name,
            'leader': obj.leader,
            'tester': obj.tester,
            'programmer': obj.programmer,
            'code': 1,
            'msg': '创建成功'
        }

        return JsonResponse(python_dict, status=201)


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
    def get(self,request,pk):
        """获取项目详情"""
        # （1）步骤一：校验参数，校验参数pk是否存在
        try:
            obj=Projects.objects.get(id=pk) # get：结果没有或返回多条结果都会报错
        except Exception as e:
            result = {
                'msg': '参数有误',
                'code': 0
            }
            return JsonResponse(result, status=400)

        # （2）步骤二：从数据库中获取模型类对象数据
        python_dict = {
            'id': obj.id,
            'name': obj.name,
            'desc': obj.desc,
            'code': 1,
            'msg': '获取成功'
        }
        # （3）步骤三：向前端返回json格式的数据
        return JsonResponse(python_dict)

    def put(self,request,pk):
        """更新项目"""
        # （1）步骤一：校验pk值否存在，并获取待更新的模型类对象
        try:
            obj=Projects.objects.get(id=pk) # get：结果没有或返回多条结果都会报错
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
        # if ('name' not in python_data) or ('leader' not in python_data):
        #     #  判断name或leader不在python_data中，则报错误
        #     result = {
        #         'msg': '参数有误',
        #         'code': 0
        #     }
        #     return JsonResponse(result, status=400)

        # （3）步骤三：更新操作
        # 如果前端传空就更新，如果不为空则更新
        obj.name=python_data.get('name') or obj.name
        obj.leader=python_data.get('leader') or obj.leader
        obj.tester = python_data.get('tester') or obj.tester
        obj.programmer = python_data.get('programmer') or obj.programmer
        obj.desc = python_data.get('desc') or obj.desc
        # 或
        # Projects.objects.filter(id=pk).update(**python_data)

        # 保存
        obj.save()

        # （4）步骤四：向前端返回json格式的数据

        python_dict = {
            'id': obj.id,
            'name': obj.name,
            'leader': obj.leader,
            'tester': obj.tester,
            'code': 1,
            'msg': '更新成功'
        }

        return JsonResponse(python_dict, status=201)

    def delete(self,request,pk):
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
        python_data={
            'msg':'删除成功',
            'code':1
        }
        return JsonResponse(python_data,status=200)