# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : serializers.py
# @Time         : 2020/7/2 11:51

from rest_framework import serializers

class ProjectsSerializer(serializers.Serializer): # 继承serializers中的Serializer
    name=serializers.CharField(max_length=200,label='项目名称',help_text='项目名称')
    leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人')
    tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员')
    # label：人性化的说明
    # help_text：API接口的中文提示
