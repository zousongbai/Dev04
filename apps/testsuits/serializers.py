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
from .models import Testsuits
from projects.models import Projects
from interfaces.models import Interfaces
from utils.common import datetime_fmt
from utils import validates


def validate_include(value):
    # 正则：以左边的方括号开头，以右边的方括号结尾，里面必须是数字，数字至少一位
    # ^：以什么开头。*：以什么结尾
    obj = re.match(r'^\[\d+(, *\d+)*\]$', value) # (, *\d+):*号表示前面的空格可有可无
    # 如果没有匹配成功
    if obj is None:
        raise serializers.ValidationError('参数格式有误')
    # 如果匹配成功
    else:
        res = obj.group()
        try:
            data = eval(res)
        except:
            raise serializers.ValidationError('参数格式有误')
        # 如果数据没有问题，列表是一个正常的列表格式，则进行for循环迭代
        for item in data:
            # 去接口表去查询接口id是否存在
            if not Interfaces.objects.filter(id=item).exists():
                raise serializers.ValidationError(f'接口id【{item}】不存在')

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
                # 'write_only': True
                'validators': [validate_include]
            },
        }

    def create(self, validated_data):
        project = validated_data.pop('project_id')
        validated_data['project'] = project
        # testsuit = Testsuits.objects.create(**validated_data)
        # return testsuit
        return super().create(validated_data)


    def update(self, instance, validated_data):
        # 如果project_id在validated_data字典中
        if 'project_id' in validated_data:
            # 如果有，则将project_id删除
            project = validated_data.pop('project_id')
            # 再创建一个project_id
            validated_data['project'] = project
            return super().update(instance, validated_data)


class TestsuitsRunSerializer(serializers.ModelSerializer):
    """
    通过套件来运行测试用例序列化器
    """
    env_id = serializers.IntegerField(write_only=True,
                                      help_text='环境变量ID',
                                      validators=[validates.is_exised_env_id])

    class Meta:
        model = Testsuits
        fields = ('id', 'env_id')

