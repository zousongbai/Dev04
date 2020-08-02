# -*- coding    : utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : base_model.py
# @Time         : 2020/8/2 11:05

from django.db import models
class BaseModel(models.Model):
    """该类是提取公共的字段，专门给其他类继承的，不会去创建表"""
    # 抽出公共的字段：create_time、update_time
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')

    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        # abstract指定在迁移的时候不创建表
        # 只要abstract：设置为True的时候，在迁移的时候，就不会创建BaseModel表
        abstract=True
