# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : urls.py
# @Time         : 2020/6/19 14:05

from django.urls import path
# 导入类视图
from projects import views
# 导入路由器
from rest_framework.routers import DefaultRouter, SimpleRouter

# 定义SimpleRouter路由对象　
# router = SimpleRouter()
# DefaultRouter相比SimpleRouter，自动添加了一条路径的路由/->：可浏览器的api页面
# 使用DefaultRouter路由器
router = DefaultRouter()

# 使用路由对象.register()方法，来进行注册
# ①第一个参数：指定路由前缀，通用方式：r'子应用名小写'
# ②第二个参数：指定视图集类即可，不要调用.as_view()方法
router.register(r'projects', views.ProjectsViewSet, basename=None)
# prefix：路由前缀，如：r'projects/'
# viewset：视图集，如：views.ProjectsViewSet
urlpatterns = [
    # path('projects/',views.ProjectsViewSet.as_view())
    # # （1）继承ViewSet之后，支持在定义路由时指定请求方法与action的映射
    # # （2）as_view需要接收一个字典
    # # （3）key为请求方法名，value为指定需要调用的action
    # path('projects/',views.ProjectsViewSet.as_view(
    #     {   # 请求方法与指定的action一一映射
    #         'get':'list',
    #         'post':'create',
    #     }
    # )),
    #
    # path('projects/names/',views.ProjectsViewSet.as_view(
    #     {   # 请求方法与指定的action一一映射
    #         'get':'names', # 指定get方法请求，并且url是projects/names/就会访问names
    #
    #     }
    # )),
    #
    # path('projects/<int:pk>/',views.ProjectsViewSet.as_view(
    #     {
    #         # 请求方法与指定的action一一映射
    #         'get':'retrieve',
    #         'put':'update',
    #         'delete':'destroy',
    #     }
    # )),
    #
    # # 获取项目的接口数据
    # path('projects/<i:pk>/interfaces/nt',views.ProjectsViewSet.as_view(
    #     {
    #         # 请求方法与指定的action一一映射
    #         'get':'interfaces'
    #     }
    # )),
]
# url设计的时候，有时候要传递id，有时候不需要传递id，怎样解决

# 使用路由对象.urls属性来获取自动生成的路由条目，往往为列表
# 需要将这个列表添加到urlpatterns
urlpatterns += router.urls
