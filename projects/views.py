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
        # project_obj = Projects(name='xxx项目2', leader='xxx项目负责人2',
        #                        tester='xxx测试2', programmer='xxx研发2')
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
        # project_obj=Projects.objects.get(id=1)
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
        # project_obj=Projects.objects.get(id=1)
        # # （2）步骤二：再删除，不需要提交，会自动提交
        # one=project_obj.delete()


        # # 1.2、可以使用模型类名.object.filter().delete()：即先查询出来，再调用delete()方法
        # project_obj=Projects.objects.filter(id=2).delete()

        # 五、查询（C）　
        # 1、使用object管理器来查询　
        # 1.1、get方法查询：
        # ①一般只能使用主键或者唯一键作为查询条件。
        # ②get方法，如果查询的记录为空和多条记录，那么会抛出异常。
        # ③返回的模型类对象，会自动提交，不需要save方法
        # project_obj=Projects.objects.get(id=1)
        #



        # 1.2、all()方法：获取所有的记录　　
        # ①返回QuerySet查询集对象
        # ②查询集对象类似于列表，支持列表中的某些操作
        # ③支持数字索引取值（负索引不支持）、切片（返回QuerySet查询集对象）
        # ④支持for循环迭代，每次迭代取出一个模型类对象
        # ⑤QuerySet查询集对象.first()获取第一个记录，QuerySet查询集对象.last()方法获取最后一条记录
        # ⑥QuerySet查询集对象.count()方法，获取查询集中数据记录条数
        # ⑦支持惰性查询：只有真正去使用数据时，才会去数据库中执行sql语句，为了性能要求
        # ⑧支持链式调用
        # project_obj=Projects.objects.all()


        # 1.3、filter方法获取某些数量的记录　　
        # ①filter支持多个过滤表达式，格式：字段名__过滤表达式
        # 1）字段名__startswith：过滤以xxx开头的字符串
        # 2）字段名__istartswith：忽略大小写，过滤以xxx开头的字符串
        # 3）字段名__endswith：过滤以xxx结尾的字符串
        # 4）字段名__iendswith：忽略大小写，过滤以xxx结尾的字符串
        # 5）字段名__gt：大于，__gte：大于等于，__le：小于，__lte：小于等于
        # 6）字段名 = 条件与字段名__exact等价，在django ORM中有一个内置的变量pk，为数据库模型类的主键别名
        # 7）__contains、__icontains、__in、__isnull
        # 8)如果没有指定的记录，会返回空查询集
        # Projects.objects.filter()

        # ②exclude与filter是反向关系，与filter条件一样
        # Projects.objects.exclude()
        # Projects.objects.raw() # 原生的sql语句
        return HttpResponse('<h2>POST请求：欢迎{}!</h2>')


    def put(self, request, pk):
        # return HttpResponse('<h2>PUT请求：欢迎进入首页</h2>')
        one_dict = '{"name":"小青年","age":18}'
        return HttpResponse(one_dict, content_type='application/json', status=201)

    def delete(self, request, pk):
        return HttpResponse('<h2>DELETE请求：欢迎进入首页</h2>')
