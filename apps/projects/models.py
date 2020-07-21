from django.db import models

# （1）步骤一：数据模型类，需要继承Model父类或者Model子类，不继承就不是数据模型类，就是普通的类
class Projects(models.Model):
    id=models.AutoField(primary_key=True)

    # ①项目名称
    name=models.CharField(max_length=200,verbose_name='项目名称',help_text='项目名称',unique=True)

    # ②项目经理的信息
    leader=models.CharField(max_length=50,verbose_name='项目负责人',help_text='项目负责人')

    # ③测试员信息
    tester=models.CharField(max_length=50,verbose_name='测试人员',help_text='测试人员')

    # ④程序员
    programmer=models.CharField(max_length=50,verbose_name='开发人员',help_text='开发人员')

    # ⑤没有使用长度限制
    desc=models.TextField(verbose_name='项目简介',help_text='项目简介',null=True,blank=True,default='xxx简介')

    # ⑥DateTimeField可以添加auto_now_add选项，Django会自动添加创建记录时的时间
    create_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间',help_text='创建时间')


    # ⑦DateTimeField可以添加auto_now选项，Django会自动添加更新记录时的时间
    update_time=models.DateTimeField(auto_now=True,verbose_name='更新时间',help_text='更新时间')



    class Meta: # 类名固定

        db_table='tb_projects'

        # ⑩指定表的个性化描述
        verbose_name='项目表'


    # （4）步骤四：创建完数据库模型类之后，需要迁移才能生成数据表
    # ①生成迁移脚本，放在projects/migrations目录中：python manage.py makemigrations
    # ②执行迁移脚本：python manage.py migrate


    def __str__(self):
        """打印对象的时候，会自动返回，并且返回一定时字符串"""
        return f"<{self.name}>" # 把项目名称填充称为一个字符串后返回
