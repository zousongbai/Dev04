from rest_framework import serializers
from rest_framework import validators

from interfaces.models import Interfaces
from testcases.models import Testcases
from utils import common, validates


class InterfacesProjectsModelSerializer(serializers.ModelSerializer):
    # 项目名称
    project = serializers.StringRelatedField(label='所属项目', help_text='所属项目')
    # 项目id
    pid = serializers.IntegerField(label='所属项目id', help_text='所属项目id', write_only=True,
                                   validators=[validates.is_exised_project_id])
    # 接口id
    iid = serializers.IntegerField(label='所属接口id', help_text='所属接口id', write_only=True,
                                   validators=[validates.is_exised_interface_id])

    class Meta:
        model = Interfaces
        fields = ('name', 'pid', 'iid')

    def validate(self, attrs):
        """多字段的灵活校验"""
        # 项目id
        pid = attrs.get('pid')
        # 接口id
        iid = attrs.get('iid')
        if not Interfaces.objects.filter(id=iid, project_id=pid).exists():
            raise serializers.ValidationError('所属项目id与接口id不匹配')


class TestcasesModelSerializer(serializers.ModelSerializer):
    interface = InterfacesProjectsModelSerializer(label='所属项目和接口', help_text='所属项目和接口')

    class Meta:
        model = Testcases
        # 排除update_time、create_time
        exclude = ('update_time', 'create_time')

        extra_kwargs = {
            'request': {
                'write_only': True,
            },
        }

    def create(self, validated_data):
        """创建用例"""
        # 先删除interface，再获取iid
        iid = validated_data.pop('interface').get('iid')
        validated_data['interface_id'] = iid
        # 调用父类create()方法
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """更新用例"""
        iid = validated_data.pop('interface').get('iid')
        validated_data['interface_id'] = iid
        return super().update(instance, validated_data)
