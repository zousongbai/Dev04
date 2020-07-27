# 导入数据库
from django.contrib.auth.models import User
# 继承rest_framework视图中的APIView
from rest_framework.views import APIView
# 导入序列化器类
from .serializers import RegisterSerializer
# 导入Response
from rest_framework.response import Response
# 导入状态码
from rest_framework import status


class UserView(APIView):

    def post(self, request, *args, **kwargs):
        # 创建序列化器类serializer对象
        serializer = RegisterSerializer(data=request.data)
        # 对序列化器类进行校验
        serializer.is_valid(raise_exception=True)
        # 校验成功之后，再调用save()方法
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UsernameIsExitedView(APIView):
    """
    针对简单的接口：不用定义序列化器类、不需要继承GenericViewSet
    """
    def get(self,request,username):

        # 去查询，用户名是否已经注册：返回查询集，如果查询集有内容，那么count不为0，
        count=User.objects.filter(username=username).count()
        one_dict={
            'username':username,
            'count':count,
        }

        # 将查询的数量返回给前端
        return Response(one_dict)

class EmailIsExitedView(APIView):
    """
    针对简单的接口：不用定义序列化器类、不需要继承GenericViewSet
    """
    def get(self,request,email):

        # 去查询，邮箱是否已经注册：返回查询集，如果查询集有内容，那么count不为0，
        count=User.objects.filter(email=email).count()
        one_dict={
            'email':email,
            'count':count,
        }

        # 将查询的数量返回给前端
        return Response(one_dict)
