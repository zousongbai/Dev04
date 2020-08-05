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
from testcases.models import Testcases
from configures.models import Configures
from utils import common


# 使用模型序列化器类：简化序列化器类中字段的创建
# 需要继承ModelSerializer
class InterfacesModelSerializer(serializers.ModelSerializer):

    # project：项目名称
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    # 项目ID：只需要输出
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(),
                                                    label='项目id', help_text='项目id',
                                                    write_only=True)

    # 在定义模型序列化器类时，需要指定根据哪个模型类来生成这些字段
    class Meta:  # 类名固定
        # 需要在Meta内部类这两个指定model类属性：需要按照哪一个模型类创建
        # 指定要生成的模型
        model=Interfaces
        # fields类属性来指定，模型类中哪些字段需要输入或输出
        # 指定当前模型类的字段
        # 将模型类所有的字段都生成序列化器类中的字段
        fields = ('id', 'name', 'tester', 'create_time', 'desc', 'project', 'project_id')

        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': common.datetime_fmt()
            }
        }

    def create(self, validated_data):
        project = validated_data.pop('project_id')
        validated_data['project'] = project
        # Interfaces.objects.create(project_id=1)
        # Interfaces.objects.create(project=某个项目对象)
        # interface = Interfaces.objects.create(**validated_data)
        # return interface
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project

        return super().update(instance, validated_data)


class TestcasesNamesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Testcases
        fields = ('id', 'name')


class TestcasesByInterfaceIdModelSerializer(serializers.ModelSerializer):
    testcases = TestcasesNamesModelSerializer(many=True, read_only=True)

    class Meta:
        model = Interfaces
        fields = ('testcases', )


class ConfiguresNamesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configures
        fields = ('id', 'name')


class ConfiguresByInterfaceIdModelSerializer(serializers.ModelSerializer):
    configures = ConfiguresNamesModelSerializer(many=True, read_only=True)

    class Meta:
        model = Interfaces
        fields = ('configures', )


