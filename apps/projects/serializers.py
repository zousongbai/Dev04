# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : serializers.py
# @Time         : 2020/7/2 11:51

from rest_framework import serializers
# 导入内置的校验器
from rest_framework import validators
# 导入模型类
from .models import Projects
# 导入Interfaces
from interfaces.models import Interfaces

from interfaces.serializers import InterfacesModelSerializer
from utils.datetime_fmt import datetime_fmt

class InterfacesNamesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interfaces
        fields = ('id', 'name')

# 使用模型序列化器类：简化序列化器类中字段的创建
# （1）需要继承ModelSerializer
class ProjectsModelSerializer(serializers.ModelSerializer):

    # 在定义模型序列化器类时，需要指定根据哪个模型类来生成这些字段
    class Meta:  # 类名固定
        # 需要在Meta内部类这两个指定model类属性：需要按照哪一个模型类创建
        # 指定要生成的模型
        model=Projects

        # 把需要排除的字段放在exclude中，过滤不生成的字段，不参与输入也不参与输出
        exclude=('update_time',)

        extra_kwargs = {
            'create_time': {
                'read_only': False,
                # 'format': common.datetime_fmt(),
            },

        }

class ProjectsNameModelSerializer(serializers.ModelSerializer):
    """只返回id和name"""
    class Meta:
        # 指定要生成的模型
        model = Projects

        # 只需要id和name
        fields=('id','name')

class InterfacesByProjectIdModelSerializer(serializers.ModelSerializer):
    interfaces = InterfacesNamesModelSerializer(many=True, read_only=True)

    class Meta:
        model = Projects
        fields = ('interfaces', )

class InterfacesByProjectsIdModelSerializer1(serializers.ModelSerializer):
    """通过项目id获取接口信息：解决分页问题"""
    # interfaces=InterfacesNameModelSerializer(many=True,read_only=True)

    # 在定义模型序列化器类时，需要指定根据哪个模型类来生成这些字段
    class Meta:  # 类名固定
        # 需要在Meta内部类这两个指定model类属性：需要按照哪一个模型类创建
        # 指定要生成的模型
        model=Interfaces
        # fields类属性来指定，模型类中哪些字段需要输入或输出
        fields = ('id','name')
