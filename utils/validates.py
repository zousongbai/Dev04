from rest_framework import serializers

from projects.models import Projects
from interfaces.models import Interfaces


def is_exised_project_id(value):
    """
    校验项目id是否存在
    :param value:
    :return:
    """
    if not Projects.objects.filter(id=value).exists():
        raise serializers.ValidationError('项目id不存在')


def is_exised_interface_id(value):
    """
    校验接口id是否存在
    :param value:
    :return:
    """
    if not Interfaces.objects.filter(id=value).exists():
        raise serializers.ValidationError('接口id不存在')
