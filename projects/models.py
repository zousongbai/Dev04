from django.db import models

# Create your models here.
# 1、可以在子应用projects/models.py文件中，来定义数据模型
# 2、一个数据模型类对应一个数据表
# 3、数据模型类，需要继承Model父类或者Model子类，不继承就不是数据模型类，就是普通的类
# 4、在数据模型类中，添加的类属性（Field对象）来对应数据表中的字段
# （1）步骤一：数据模型类，需要继承Model父类或者Model子类，不继承就不是数据模型类，就是普通的类
class Projects(models.Model):
    # （2）步骤二：
    # ①模型类名：为子应用名首字母大写，即Projects
    # ②需要继承models当中的Model

    # （3）步骤三：以类属性的形式添加数据表的字段
    # ①项目名称
    name=models.CharField(max_length=200)
    # 备注：
    # 1）CharField：对应数据库的字符串varchar
    # 2）并设置字符串的最大长度

    # ②项目经理的信息
    leader=models.CharField(max_length=50)


    # （4）步骤四：往指定的数据表里面自动生成数据表信息
    # ①makemigrations： 迁移脚本，即：python manage.py makemigrations
    # ②migrate：创建数据表，即python manage.py migrate


