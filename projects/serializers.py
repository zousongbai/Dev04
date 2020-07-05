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

# 继承serializers中的Serializer
class ProjectsSerializer(serializers.Serializer): # 类名：建议使用：模型类对象+Serializer

    """
    可以定义序列化器类，来实现序列化和反序列化操作
    （1）一定要继承serializers.Serializer或者Serializer的子类
    （2）默认情况下，可以定义序列化器字典字段，序列化器字段名要与模型类中字段名相同
    （3）默认情况下，定义几个序列化器字段，那么就会返回几个数据（到前端，序列化输出的过程），前端也必须得传递这几个字段（反序列化过程）
    （4）CharField、BooleanField、IntegerField与模型类中的字段类型一一对应
    （5）required参数默认为None，指定前端必须得传此字段，如果设置为False的话，前端可以不传此字段
    （6）label和help_text->与模型类的verbose_name和help_text一一对应
    （7）alow_null指定前端传递参数时可以传空
    （8）CharField字段拥有max_length属性指定该字段不能超过的字节长度

    """

    # （11）如果某个字段，即没有read_only，也没有write_only，说明此字段既需要反序列化输入，也需要序列化输出
    name=serializers.CharField(max_length=10,label='项目名称',help_text='项目名称',min_length=2,
                               validators=[validators.UniqueValidator(queryset=Projects.objects.all(),message='项目名称已存在')])
    # 备注：
    # ①validators：需要指定一个列表，
    # ②UniqueValidator：专门用来做唯一性的校验，
    # 1)第一个参数queryset：是所有项目的查询集
    # 2）第二个参数message：校验失败后的报错信息



    # （10）如果某个字段指定read_only=True，那么此字段，前端在创建数据时（反序列化过程）可以不用传，但是一定会输出（序列化过程）
    leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人',read_only=True)
    # （12）字段不能同时指定read_only=True，required=True
    # leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人', read_only=True,required=True)



    # （9）如果某个字段指定了write_only = True，那么此字段只能进行反序列化输入，而不会输出（创建数据时必须得传，但是不返回）
    # tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员', write_only=True)

    # （14）可以给字段添加error_messages参数，为字典类型，字典的key为校验的参数名，值为校验失败之后的错误提示
    tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员', write_only=True,
                                   error_messages={'required':'该字段必传','max_length':'长度不能超过200个字节'})
    # （13）字段不能同时指定write_only=True，read_only=True
    # tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员', write_only=True,read_only=True)


    # label：人性化的说明
    # help_text：API接口的中文提示
    # models中只能指定最大长度，序列化器中既可以指定最大长度，也可以指定最小长度
