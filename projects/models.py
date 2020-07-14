from django.db import models


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
# 8、models中字段对应MySQL的字段
# （1）CharField->varchar
# （2）IntegerField->int
# （3）TextField->text
# 9、verbose_name：添加中文中文提示，为个性化信息
# 10、help_text帮助文本信息，在api接口文档平台和admin后端站点中会用于提示，往往跟verbose_name一致
# 11、unique：用于指定唯一键，默认为False
# 12、CharField：至少要指定一个max_length必传参数，代表此字段的最大长度，不能为负数
# 13、null：指定数据在保存时是否可以为空，默认不能为空，如果null=True，那么可以为空值
# 14、blank：指定前端用户在创建数据时，是否需要传递，默认需要传递，如果不传递，需要将blank设置为True
# 15、default为某个字段指定默认值，往往会跟blank一起使用
# 16、DateTimeField可以添加auto_now_add选项，Django会自动添加创建记录时的时间
# 17、DateTimeField可以添加auto_now选项，Django会自动添加更新记录时的时间
# 18、执行迁移脚本之后，生成的数据表名，默认为：子应用名_模型类名小写
# 19、可以在模型类下定义Meta子类，Meta子类名称固定
# 20、可以使用db_table类属性，来指定表名
# 21、指定表的个性化描述


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
