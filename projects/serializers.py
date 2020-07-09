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

from interfaces.serializers import InterfacesModelSerializer

def is_name_contain_x(value):
    """
    校验name字段是否包含x
    :param value:前端输入的待校验的值，即前端输入了name值，会自动传递给校验函数的第一个参数value
    :return:
    """
    if 'x' in value:
        # 如果校验失败，一定要抛出ValidationError异常类对象，第一个参数可以指定具体的报错信息
        # 如果x包含在value里面，则抛出异常
        raise serializers.ValidationError('项目名称中不能包含x')

# 继承serializers中的Serializer
class ProjectsSerializer(serializers.Serializer): # 类名：建议使用：模型类对象+Serializer


    # （11）如果某个字段，即没有read_only，也没有write_only，说明此字段既需要反序列化输入，也需要序列化输出
    name=serializers.CharField(max_length=10,label='项目名称',help_text='项目名称',min_length=2,
                               validators=[validators.UniqueValidator(queryset=Projects.objects.all(),message='项目名称已存在'),is_name_contain_x])

    # （10）如果某个字段指定read_only=True，那么此字段，前端在创建数据时（反序列化过程）可以不用传，但是一定会输出（序列化过程）
    leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人',read_only=True)

    # （14）可以给字段添加error_messages参数，为字典类型，字典的key为校验的参数名，值为校验失败之后的错误提示
    tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员', allow_blank=True,read_only=True,
                                   error_messages={'required':'该字段必传','max_length':'长度不能超过200个字节'})

    def validate_name(self,value):
        """
        项目名称中不能包含“非常”
        :param value:
        :return:类的外面定义的校验不需要返回，类的里面定义的校验需要将这个值返回
        """
        if '非常' in value:
            raise serializers.ValidationError('项目名称中不能包含“非常”')
        return value

    def validate(self, attrs):
        """
        多字段校验，固定使用validate方法
        :param attrs:为前端输入的待校验的参数
        :return:
        """
        # if len(attrs['name'])!=8 or '测试' not in attrs['tester']:
        #     # name的长度不等于8或者“测试”不在tester内，则抛出异常
        #     raise serializers.ValidationError('项目名长度不为8或者测试人员名称中不包含“测试”')
        return attrs

    def create(self, validated_data):
        """
        创建数据：必须将创建成功的模型类对象返回
        :param validated_data:为校验通过之后的数据
        :return:
        """
        obj=Projects.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        """
        数据的更新：放在序列化器类里面，必须将更新成功的模型类对象返回
        :param instance:为待更新的模型类对象
        :param validated_data:为校验通过之后的数据
        :return:
        """
        # （3）步骤三：更新操作
        # 用校验之后的数据validated_data去获取
        instance.name = validated_data.get('name') or instance.name
        instance.leader = validated_data.get('leader') or instance.leader
        instance.tester = validated_data.get('tester') or instance.tester
        instance.programmer = validated_data.get('programmer') or instance.programmer
        instance.desc = validated_data.get('desc') or instance.desc
        # 保存
        instance.save()
        return instance

# 使用模型序列化器类：简化序列化器类中字段的创建
# （1）需要继承ModelSerializer
class ProjectsModelSerializer(serializers.ModelSerializer):
    # 如果在模型序列化器类中显示指定了模型类中的某个字段，那么会将自动生成的字段覆盖掉
    # name=serializers.CharField(max_length=20,label='项目名称',help_text='项目名称',min_length=5,
    #                            validators=[validators.UniqueValidator(queryset=Projects.objects.all(),message='项目名称已存在')])

    # # 导入locale
    # import locale  # locale：专门处理编码
    # # 将本地的语言设置为chinese
    # locale.setlocale(locale.LC_CTYPE,'chinese')
    # # 格式化字符串
    # datetime_fmt='%Y年%m月%d日 %H:%M:%S'


    # 在模型序列化器类中添加模型类中没有的字段
    email=serializers.EmailField(write_only=True) # 只输入不输出

    # 通过父表（Projects）获取子表（Interfaces）的信息
    # ①默认可以使用子表模型类名首字母小写_set，即默认名称：interfaces_set
    # interfaces_set=InterfacesModelSerializer(label='所拥有的接口',many=True)
    # 备注：因为interfaces_set是多个，所以要设置many=True

    # ②子表模型类名首字母小写_set，代表可以获取子表的信息
    # 如果某个字段返回的结果有多条，那么需要添加many=True参数
    # interfaces_set=serializers.StringRelatedField(many=True)

    # ③子表的模型类使用了related_name='interfaces'，父表序列化类的时候就不能使用interfaces_set
    interfaces=serializers.StringRelatedField(many=True)

    # 主表projects继承了ModelSerializer，不会生成子表的字段。
    # 如果要生成，则需要显示的指定，但名称有要求，子表名小写_set
    # interfaces_set = serializers.PrimaryKeyRelatedField(many=True)

    # 时间格式化输出
    # （1）方法一：返回之前进行修改
    # ①英文格式：2020-03-20
    # update_time=serializers.DateTimeField(label='更新时间',help_text='更新时间',
    #                                       format='%Y-%m-%d %H:%M:%S',required=False)

    import utils # 自定义工具
    # ②中文格式：2020年3月20日　
    update_time = serializers.DateTimeField(label='更新时间', help_text='更新时间',
                                            format=utils.datetime_fmt, required=False)

    # 在定义模型序列化器类时，需要指定根据哪个模型类来生成这些字段
    class Meta:  # 类名固定
        # （2）需要在Meta内部类这两个指定model类属性：需要按照哪一个模型类创建
        # 指定要生成的模型
        model=Projects
        # （3）fields类属性来指定，模型类中哪些字段需要输入或输出
        # 指定当前模型类的字段
        # ①将模型类所有的字段都生成序列化器类中的字段
        # fields='__all__'

        # ②定义的所有序列化器字段，必须得添加到fields元祖中，模型类中未定义的字段也需要添加
        # fields=('id','name','leader','tester','programmer','create_time','update_time','email','interfaces_set')

        fields = ( 'id', 'name', 'leader', 'tester', 'programmer', 'create_time', 'update_time', 'email', 'interfaces')

        # ③把需要排除的字段放在exclude中，过滤不生成的字段，不参与输入也不参与输出
        # exclude=('desc',)

        # 可以在read_only_fields中指定需要进行read_only=True的字段，统一指定要只输出不输入的字段，
        read_only_fields = ('id', 'desc', 'programmer')

        # 可以在extra_kwargs属性中，来定制某些字段，有的会覆盖，没有的会新增
        # 对字段添加额外的限制
        # 把需要修改的字段名作为key,value值为字典里面是修改的内容
        extra_kwargs = {
            'programmer': {
                'label': '研发人员',
                'write_only': False,
                'max_length': 10,  # 设置最大长度
                'min_length': 4,
            },
            # 'name': {
            #     'max_length': 10,
            #     'min_length': '2',
            #     'validators': [is_name_contain_x]
            # }
        }

    # email在保存数据的时候，会调用父类的create方法，
    # 父类的create方法，validated_data中包含了所有校验通过的数据，没有包含email
    # 所以直接传入email会提示报错信息
    def create(self, validated_data):
        # （1）步骤一：先pop调email
        email=validated_data.pop('email')
        # 备注：为什么要把模型类没有的字段删除？
        # 因为，如注册的功能，用户需要输入密码和确认密码，真正在保存的时候，不需要保存确认密码，但确认密码前端又必须要校验
        # 所以，基于这种场景就有必要重写create实现
        # （2）步骤二：再调用父类的create
        return super().create(validated_data)
        # return Projects.objects.create(**validated_data)

