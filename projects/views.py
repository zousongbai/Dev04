import json
from django.http import HttpResponse
from django.views import View

# 导入模型类的方法：
# 方法一：通过.models的方式进行导入
from .models import Projects  # 点：表示在view当前的路径下面
# 方法二：从子应用中的projects/models.py导入
from projects.models import Projects


# 查看生成的sql
from django.db import connection # 导入django.db中的connection，connection有一个queries属性

# 创建函数
def index_page(request):
    """
    视图函数：必须按照下面的规范：
    1、第一个参数为HttpRequest对象或者HttpRequest子类的对象,无需手动传递
    2、一般会使用request
    3、一定要返回HttpResponse对象或者HttpResponse子类对象
    :param request:
    :return:
    """
    if request.method == 'GET':
        return HttpResponse('<h2>GET请求：欢迎进入首页</h2>')
    elif request.method == 'POST':
        return HttpResponse('<h2>POST请求：欢迎进入首页</h2>')
    elif request.method == 'PUT':
        pass


def index_page2(request):
    """定义一个视图"""
    return HttpResponse('<h2>欢迎进入首页</h2>')


class IndexPage(View):  # 继承Django中的View
    """类视图"""

    def get(self, request, pk):
        """get的业务逻辑"""
        return HttpResponse('<h2>GET请求：欢迎进入首页</h2>')

    def post(self, request):
        # 二、c（create） ：创建
        # 1、创建的两种方法：
        # 1.1、使用模型类对象来创建
        # （1）步骤一：使用模型类对象来创建，会创建一个Projects模型类对象，但是还未提交
        # ①模型类的对象的属性怎样做？模型类的字段名作为参数名
        # ②id：可以不加，因为是自增的主键
        # ③create_time和update_time：自动添加
        # project_obj = Projects(name='xxx项目4', leader='xxx项目负责人4',
        #                        tester='xxx测试4', programmer='xxx研发4')
        #
        # # （2）步骤二：需要调用模型类对象的save()方法，去提交
        # project_obj.save()

        # 1.2、可以使用查询集的create方法来创建
        # （1）使用模型类名.objects.create()方法
        # （2）objects是manager对象，用于对数据进行操作
        # project_obj=Projects.objects.create(name='xxx项目5', leader='xxx项目负责人5',
        #                        tester='xxx测试5', programmer='xxx研发5')

        # 三、u（update）：更新
        # 1、更新的两种方法：
        # 1.1、先获取模型类对象，然后修改某些字段，再调用save方法保存
        # （1）步骤一：先读取。
        # ①数据表中的一条记录就是模型类的一个对象
        # ②所以读取是用：模型类名.objects.get去读取，读取后数据是模型类对象
        # 读取id为3的数据
        # project_obj=Projects.objects.get(id=3)
        #
        # # （2）步骤二：再更新
        # project_obj.name='某某知名项目'
        #
        # # （3）步骤三：调用save方法保存
        # project_obj.save()

        # 1.2、可以使用模型类名.object.filter().update(字段名=修改的值)：即先查询出来，再调用update()方法
        # （1）步骤一：查询id为2，返回查询集，Projects.objects.filter(id=2)
        # （2）步骤二：再去update修改name
        # Projects.objects.filter(id=2).update(name='某某优秀的项目')

        # 四、d（delete）：删除
        # 1、删除的两种方法
        # 1.1、可以使用模型类对象.delete()方法删除
        # （1）步骤一：先查询出来
        # project_obj=Projects.objects.get(id=3)
        # # （2）步骤二：再删除，不需要提交，会自动提交
        # one=project_obj.delete()


        # # 1.2、可以使用模型类名.object.filter().delete()：即先查询出来，再调用delete()方法
        # project_obj=Projects.objects.filter(id=2).delete()

        # 五、查询（C）　
        # 1、使用object管理器来查询　
        # （1）get方法查询：
        # ①一般只能使用主键或者唯一键作为查询条件。
        # ②get方法，如果查询的记录为空和多条记录，那么会抛出异常。
        # ③返回的模型类对象，会自动提交，不需要save方法
        project_obj=Projects.objects.get(id=1)

        Projects.objects.filter(id__gte=2) # id__gte：打印等于

        Projects.objects.filter(name)
        return HttpResponse('<h2>POST请求：欢迎{}!</h2>')


    def put(self, request, pk):
        # return HttpResponse('<h2>PUT请求：欢迎进入首页</h2>')
        one_dict = '{"name":"小青年","age":18}'
        return HttpResponse(one_dict, content_type='application/json', status=201)

    def delete(self, request, pk):
        return HttpResponse('<h2>DELETE请求：欢迎进入首页</h2>')
