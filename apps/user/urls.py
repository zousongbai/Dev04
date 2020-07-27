from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', views.UserView.as_view()),
    # 路径用正则表达式：对username进行比较复杂的校验，所以path就不支持，所以需要re_path
    re_path(r'^(?P<username>\w{6,20})/count/$', views.UsernameIsExitedView.as_view()),
    # ^：以什么开头
    # $：以什么结尾
    # 外面的括号进行分组，分组取的名字是username
    # w：代表可以使用字母、数字、下划线
    # w{6,20}：用户名的长度为6-20位
    re_path(r'^(?P<email>[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+)/count/$', views.EmailIsExitedView.as_view())
]
