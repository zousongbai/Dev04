# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : serializers.py
# @Time         : 2020/7/2 11:51

from rest_framework import serializers
# 导入内置的校验器
from rest_framework import validators
# 导入模型类
from .models import Testsuits
from projects.models import Projects
from utils.common import datetime_fmt

class TestsuitsModelSerializer(serializers.ModelSerializer):

    # project：项目名称
    project=serializers.StringRelatedField(label='所属项目名称',help_text='所属项目名称')
    project_id=serializers.PrimaryKeyRelatedField(label='所属项目id',help_text='所属项目id',
                                                  queryset=Projects.objects.all(),write_only=True)

    # 在定义模型序列化器类时，需要指定根据哪个模型类来生成这些字段
    class Meta:  # 类名固定
        # 指定要生成的模型
        model=Testsuits
        # fields类属性来指定，模型类中哪些字段需要输入或输出
        fields=('id','name','project','project_id','include','create_time','update_time')
        extra_kwargs={
            'create_time':{
                # 只需要输出
                'read_only':True,
                'format':datetime_fmt()
            },
            'update_time': {
                # 只需要输出
                'read_only': True,
                'format': datetime_fmt()
            },
            'include': {
                # 只需要输入
                'write_only': True
            },
        }

    def create(self, validated_data):
        pass




