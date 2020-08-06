# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : serializers.py
# @Time         : 2020/7/2 11:51
import re
from rest_framework import serializers
# 导入内置的校验器
from rest_framework import validators
# 导入模型类
from .models import Reports
from utils.common import datetime_fmt

class ReportsModelSerializer(serializers.ModelSerializer):
    # 在定义模型序列化器类时，需要指定根据哪个模型类来生成这些字段
    class Meta:  # 类名固定
        # 指定要生成的模型
        model=Reports

        exclude = ('update_time',)

        extra_kwargs = {
            'create_time': {
                'format': datetime_fmt()
            },
            'html': {
                # 不需要输出
                'write_only': True
            }
        }