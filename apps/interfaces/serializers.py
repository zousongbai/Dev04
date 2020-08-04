# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : serializers.py
# @Time         : 2020/7/2 11:51

from rest_framework import serializers
# 导入内置的校验器
from rest_framework import validators
# 导入模型类
from .models import Interfaces
from projects.models import Projects
# from projects.serializers import ProjectsModelSerializer


# 使用模型序列化器类：简化序列化器类中字段的创建
# 需要继承ModelSerializer
class InterfacesModelSerializer(serializers.ModelSerializer):

    # project：项目名称
    project=serializers.StringRelatedField()
    # 项目ID：只需要输出
    # project_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Projects.objects.all())
    # 或使用IntegerField，与PrimaryKeyRelatedField作用是一样的，但要指定校验器validators，不能指定查询集
    # project_id = serializers.IntegerField(write_only=True, validators=[])

    # 在定义模型序列化器类时，需要指定根据哪个模型类来生成这些字段
    class Meta:  # 类名固定
        # 需要在Meta内部类这两个指定model类属性：需要按照哪一个模型类创建
        # 指定要生成的模型
        model=Interfaces
        # fields类属性来指定，模型类中哪些字段需要输入或输出
        # 指定当前模型类的字段
        # 将模型类所有的字段都生成序列化器类中的字段
        fields='__all__'
    def create(self, validated_data):
        pass




