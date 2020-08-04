from django.db import models

from utils.base_models import BaseModel


class DebugTalks(BaseModel):
    # id自动添加
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    name = models.CharField('debugtalk文件名称', max_length=200, default='debugtalk.py', help_text='debugtalk文件名称')
    # debugtalk：存放的是debugtalk.py文件的代码
    debugtalk = models.TextField(null=True, default='#debugtalk.py', help_text='debugtalk.py文件')
    # 指定项目表
    project = models.OneToOneField('projects.Projects', on_delete=models.CASCADE,
                                   related_name='debugtalks', help_text='所属项目')

    class Meta:
        db_table = 'tb_debugtalks'
        verbose_name = 'debugtalk.py文件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
