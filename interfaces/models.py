from django.db import models

# 表与表之间有哪些关系？
# （1）一对一：models.OneToOneField
# （2）一对多：models.ForeignKey。“一”叫做父表（项目表），“多”叫做从表（子表，接口表），创建多表的时候，是在子表创建
# （3）多对多：models.OneToOneField
class Interfaces(models.Model):
    name=models.CharField(verbose_name='接口名称',max_length=200,unique=True,help_text='接口名称')
    # ForeignKey指定外键字段
    # ①第一个参数为必传参数，为父表模型类的引用（可以为模型类名或者使用'应用名.父表模型类名'）
    # ②第二个参数为必传参数on_delete，指定父表记录被删除之后，子表中对应的记录的处理方式
    # 1）models.CASCADE：父表记录被删除，子表自动删除
    # models.ForeignKey('projects.Projects', on_delete=models.CASCADE)
    # 2）models.SET_NULL,null=True：父表记录删除，子表自动设置为null
    # models.ForeignKey('projects.Projects',on_delete=models.SET_NULL,null=True)

    projects=models.ForeignKey('projects.Projects', on_delete=models.CASCADE,verbose_name='所属项目',help_text='所属项目')
    # 备注：
    # ①第一个参数：'projects.Projects'：应用名.父表模型类名
    # ②变量名为父表的模型类小写

    tester=models.CharField(verbose_name='测试人员',max_length=50,help_text='测试人员')
    desc=models.CharField(verbose_name='简要描述',max_length=200,null=True,blank=True,help_text='简要描述')

    class Meta:
        db_table='tb_interfaces'
        verbose_name='接口信息'
        # 数据库模型类的复数，像英文中的apple->apples
        verbose_name_plural=verbose_name

    def __str__(self):
        """打印对象的时候，会自动返回，并且返回一定时字符串"""
        return f"<{self.name}>"  # 把项目名称填充称为一个字符串后返回
