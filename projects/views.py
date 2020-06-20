import json
from django.http import HttpResponse
from django.views import View


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

    def post(self, request, pk):
        # (1)可以使用request.POST的方法，去获取application/x-www-urlencoded类型参数
        # (2)可以使用request.body的方法，去获取application/json类型参数
        # （3）方法三：可以使用request.META方法，获取请求头参数，key为HTTP_请求头的大写
        data_dic = json.loads(request.body, encoding='utf-8')
        return HttpResponse('<h2>POST请求：欢迎{}!</h2>'.format(data_dic['name']))

    def put(self, request, pk):
        # return HttpResponse('<h2>PUT请求：欢迎进入首页</h2>')
        one_dict='{"name":"小青年","age":18}'
        return HttpResponse(one_dict,content_type='application/json',status=201)

    def delete(self, request, pk):
        return HttpResponse('<h2>DELETE请求：欢迎进入首页</h2>')
