# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : serializers.py
# @Time         : 2020/7/2 11:51

from rest_framework import serializers

# 导入模型类
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.serializers import jwt_payload_handler,jwt_encode_handler

class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(label='确认密码', help_text='确认密码',
                                             min_length=6, max_length=20,
                                             write_only=True,
                                             error_messages={
                                                 'min_length': '仅允许6~20个字符的确认密码',
                                                 'max_length': '仅允许6~20个字符的确认密码', })
    # 需要加read_only=True，因为token不需要输入
    token = serializers.CharField(label='生成token', read_only=True)

    class Meta:
        """固定用法"""
        model = User
        fields = ('id', 'username', 'password', 'email', 'password_confirm', 'token')
        extra_kwargs = {
            'username': {
                'label': '用户名',
                'help_text': '用户名',
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许6-20个字符的用户名',
                    'max_length': '仅允许6-20个字符的用户名',
                }
            },
            'email': {
                'label': '邮箱',
                'help_text': '邮箱',
                'write_only': True,
                'required': True,
                # 添加邮箱重复校验
                'validators': [UniqueValidator(queryset=User.objects.all(), message='此邮箱已注册')],
            },
            'password': {
                'label': '密码',
                'help_text': '密码',
                'write_only': True,
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许6-20个字符的密码',
                    'max_length': '仅允许6-20个字符的密码',
                }
            }
        }

    def validate(self, attrs):
        """确认密码的校验"""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError('密码与确认密码不一致')

        return attrs

    def create(self, validated_data):
        # 用户创建的时候，需要去掉确认密码
        validated_data.pop('password_confirm')
        # 创建user模型对象：调用create_user之后会创建用户的数据，同时将密码进行加密
        user = User.objects.create_user(**validated_data)
        # 备注：因为调用create_user后，会返回user对象，所以用user接收即可

        # 创建token
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        # 将user当中的模型类对象添加一个token属性，然后再序列化输出的时候就有token
        user.token = token
        return user
