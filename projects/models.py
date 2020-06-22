from django.db import models

# Create your models here.
# 1、可以在子应用projects/models.py文件中，来定义数据模型
# 2、一个数据模型类对应一个数据表
# 3、数据模型类，需要继承Model父类或者Model子类，不继承就不是数据模型类，就是普通的类
# 4、在数据模型类中，添加的类属性（Field对象）来对应数据表中的字段
# 5、创建完数据库模型类之后，需要迁移才能生成数据表
# ①生成迁移脚本，放在projects/migrations目录中：python manage.py makemigrations
# ②执行迁移脚本：python manage.py migrate
# ③如果不添加选项，那么会将所有子应用进行迁移
# 6、会自动创建字段名为id的类属性，自增、主键、非空
# 7、只要某一个字段中primary_key=True，那么django就不会自动创建id字段，会使用自定义的

# （1）步骤一：数据模型类，需要继承Model父类或者Model子类，不继承就不是数据模型类，就是普通的类
class Projects(models.Model):
    # （2）步骤二：
    # ①模型类名：为子应用名首字母大写，即Projects
    # ②需要继承models当中的Model

    # （3）步骤三：以类属性的形式添加数据表的字段
    # 7、只要某一个字段中primary_key=True，那么django就不会自动创建id字段，会使用自定义的
    id=models.AutoField(primary_key=True)
    # ①项目名称
    name=models.CharField(max_length=200)
    # 备注：
    # 1）CharField：对应数据库的字符串varchar
    # 2）并设置字符串的最大长度

    # ②项目经理的信息
    leader=models.CharField(max_length=50)


    # （4）步骤四：创建完数据库模型类之后，需要迁移才能生成数据表
    # ①生成迁移脚本，放在projects/migrations目录中：python manage.py makemigrations
    # ②执行迁移脚本：python manage.py migrate



