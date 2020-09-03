# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : serializers.py
# @Time         : 2020/7/2 11:51

from rest_framework import serializers
# 导入内置的校验器
from rest_framework import validators
# 导入模型类
from .models import Envs
from utils import common


# 使用模型序列化器类：简化序列化器类中字段的创建
# （1）需要继承ModelSerializer
class EnvsModelSerializer(serializers.ModelSerializer):

    # 在定义模型序列化器类时，需要指定根据哪个模型类来生成这些字段
    class Meta:  # 类名固定
        # 需要在Meta内部类这两个指定model类属性：需要按照哪一个模型类创建
        # 指定要生成的模型
        model=Envs

        # 把需要排除的字段放在exclude中，过滤不生成的字段，不参与输入也不参与输出
        exclude=('update_time',)

        extra_kwargs = {
            'create_time': {
                # 只需要输出不需要输入
                'read_only': True,
                'format': common.datetime_fmt(),
            },

        }

    def create(self, validated_data):
        pass

class EnvsNamesSerializer(serializers.ModelSerializer):
    class Meta:  # 类名固定
        # 需要在Meta内部类这两个指定model类属性：需要按照哪一个模型类创建
        # 指定要生成的模型
        model=Envs

        fields=('id','name')


