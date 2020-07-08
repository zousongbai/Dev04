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
# （1）需要继承ModelSerializer
class InterfacesModelSerializer(serializers.ModelSerializer):
    # 关联字段的三种形式
    # ①会将父表的主键id值作为返回值
    # 外键关联字段：PrimaryKeyRelatedField，外键名称为模型类中的字段
    # projects = serializers.PrimaryKeyRelatedField(help_text='所属项目', label='所属项目', queryset=Projects.objects.all())
    # 备注：项目关联的ID一定要在Projects查询集里面

    # ②会将父表对应对象的__str__方法结果返回
    projects=serializers.StringRelatedField()
    # StringRelatedField的作用：在序列化输出的时候，它不会返回项目ID（即主键id），而是返回父表对应对象的打印值

    # ③会将父表对应对象的某个字段的值返回
    # slug_field：指定序列化输出的时候，显示哪一个字段
    # projects=serializers.SlugRelatedField(slug_field='leader',read_only=True)

    # 可以将某个序列化器对象定义为字段，支持Field中的所有参数
    # projects=ProjectsModelSerializer(label='所属项目信息',help_text='所属项目信息',read_only=True)

    # 在定义模型序列化器类时，需要指定根据哪个模型类来生成这些字段
    class Meta:  # 类名固定
        # （2）需要在Meta内部类这两个指定model类属性：需要按照哪一个模型类创建
        # 指定要生成的模型
        model=Interfaces
        # （3）fields类属性来指定，模型类中哪些字段需要输入或输出
        # 指定当前模型类的字段
        # ①将模型类所有的字段都生成序列化器类中的字段
        fields='__all__'


