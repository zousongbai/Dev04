# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : datetime_fmt.py
# @Time         : 2020/7/16 15:55

# 导入locale
import locale  # locale：专门处理编码
import json
def datetime_fmt():
    """将时间进行格式化"""
    # 将本地的语言设置为chinese
    locale.setlocale(locale.LC_CTYPE,'chinese')
    # 格式化字符串
    datetime_fmt='%Y年%m月%d日 %H:%M:%S'
    return datetime_fmt

def generate_testcase_file(instance, env, testcase_dir_path):
    """生成yaml用例文件"""
    testcase_list = []
    config = {
        'config': {
            # 配置名称
            'name': instance.name,
            'request': {
                # 如果env空，则取出来；如果为空，则设置为空
                'base_url': env.base_url if env else ''
            }
        }
    }
    testcase_list.append(config)

    # 获取include信息
    include = json.loads(instance.include, encoding='utf-8')
    # 获取request字段
    request = json.loads(instance.request, encoding='utf-8')
    # 获取用例所属接口名称
    interface_name = instance.interface.name
