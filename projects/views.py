# 步骤一：导入HttpResponse
from django.http import HttpResponse


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
    return HttpResponse('<h2>欢迎</h2>')

def index_page2(request):
    """定义一个视图"""
    return HttpResponse('<h2>欢迎进入首页</h2>')