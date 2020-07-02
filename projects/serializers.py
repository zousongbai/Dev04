# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : serializers.py
# @Time         : 2020/7/2 11:51

from rest_framework import serializers
# 继承serializers中的Serializer
class ProjectsSerializer(serializers.Serializer): # 类名：建议使用：模型类对象+Serializer
    """
    可以定义序列化器类，来实现序列化和反序列化操作
    （1）一定要继承serializers.Serializer或者Serializer的子类
    （2）默认情况下，可以定义序列化器字典字段，序列化器字段名要与模型类中字段名相同
    （3）默认情况下，定义几个序列化器字段，那么就会返回几个数据（到前端）
    （4）CharField、BooleanField、IntegerField与模型类中的字段类型一一对应
    """

    name=serializers.CharField(max_length=200,label='项目名称',help_text='项目名称')
    leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人')
    tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员')
    # label：人性化的说明
    # help_text：API接口的中文提示
