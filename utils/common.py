# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : datetime_fmt.py
# @Time         : 2020/7/16 15:55

# 导入locale
import locale  # locale：专门处理编码
import json
import os
import yaml

from httprunner.task import HttpRunner
from httprunner.report import render_html_report
from rest_framework.response import Response
from datetime import datetime

from debugtalks.models import DebugTalks
from configures.models import Configures
from testcases.models import Testcases
from reports.models import Reports

def datetime_fmt():
    """将时间进行格式化"""
    # 将本地的语言设置为chinese
    locale.setlocale(locale.LC_CTYPE,'chinese')
    # 格式化字符串
    datetime_fmt='%Y年%m月%d日 %H:%M:%S'
    return datetime_fmt

def create_report(runner, report_name=None):
    """
    创建测试报告
    :param runner:
    :param report_name:
    :return:
    """
    # 取出start_at，并转换为时间戳
    time_stamp = int(runner.summary["time"]["start_at"])
    # 通过时间戳转换为具体的日期类型
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    # 将start_datetime进行格式化
    runner.summary['time']['start_datetime'] = start_datetime
    # duration保留3位小数
    runner.summary['time']['duration'] = round(runner.summary['time']['duration'], 3)
    # 报告名称：如果不为空，则使用report_name；如果为空，则使用start_datetime
    report_name = report_name if report_name else start_datetime
    # 重写html_report_name
    runner.summary['html_report_name'] = report_name

    # 将content的字节类型转换为字符串
    for item in runner.summary['details']:
        try:
            for record in item['records']:
                # 对时间戳进行处理
                try:
                    time_stamp = int(record['meta_data']['request']['start_timestamp'])
                    record['meta_data']['request']['start_timestamp'] = \
                        datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
                except Exception:
                    pass

                record['meta_data']['response']['content'] = record['meta_data']['response']['content']. \
                    decode('utf-8')
                record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'])

                request_body = record['meta_data']['request']['body']
                if isinstance(request_body, bytes):
                    record['meta_data']['request']['body'] = request_body.decode('utf-8')
        except Exception as e:
            continue

    # 将字典转换为json格式字符串
    summary = json.dumps(runner.summary, ensure_ascii=False)
    # 报告名称拼接成时间戳
    report_name = report_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    report_path = runner.gen_html_report(html_report_name=report_name)

    with open(report_path, encoding='utf-8') as stream:
        reports = stream.read()

    test_report = {
        'name': report_name,
        'result': runner.summary.get('success'),
        'success': runner.summary.get('stat').get('successes'),
        'count': runner.summary.get('stat').get('testsRun'),
        'html': reports,
        'summary': summary
    }
    # 创建报告的执行对象
    report_obj = Reports.objects.create(**test_report)
    # 返回报告的id
    return report_obj.id


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
    # 获取用例所属的项目名称
    project_name=instance.interface.project.name
    # 拼接项目路径，并覆盖之前的路径
    testcase_dir_path = os.path.join(testcase_dir_path, project_name)

    if not os.path.exists(testcase_dir_path):
        # 判断testcase_dir_path路径不存在，则去创建
        # mkdir：只能创建一级目录，如果前面目录不存在会报错
        # makedirs：可以创建多级目录
        os.makedirs(testcase_dir_path)

        # 生成debugtalk.py文件，放到项目根目录下。
        # 生成debugtalk.py文件需要它的源代码，其源代码在apps/debugtalks/models.py中的debugtalk字段里面
        debugtalk_obj = DebugTalks.objects.filter(project__name=project_name).first() # 取出第一个元素
        # 如果debugtalk_obj不为空，则直接取出来debugtalk字段；如果为空，则直接赋值为空字符串
        debugtalk = debugtalk_obj.debugtalk if debugtalk_obj else ''
        # 生成debugtalk.py文件
        with open(os.path.join(testcase_dir_path, 'debugtalk.py'), 'w', encoding='utf-8') as f:
            f.write(debugtalk)
        # 拼接后，再覆盖
        testcase_dir_path = os.path.join(testcase_dir_path, interface_name)
        # 创建:如果不存在,则创建;
        if not os.path.exists(testcase_dir_path):
            os.makedirs(testcase_dir_path)

        # 解析用例:如{"config":1,"testcases":[1,2,3]}
        if 'config' in include:
            # 取出配置id:config_id
            config_id = include.get('config')
            # 获取配置的模型类对象
            config_obj = Configures.objects.filter(id=config_id).first()
            # 判断模型类对象存在
            if config_obj:
                # json.loads：将字符串转换为字典
                config_request = json.loads(config_obj.request, encoding='utf-8')
                # 将config作为第一层key，request作为第二层key，base_url作为第三层key
                config_request['config']['request']['base_url'] = env.base_url if env else ''
                # 覆盖列表testcase_list当中的第一个元素
                testcase_list[0] = config_request

    # 处理前置用例
    # 如果include中有testcases，则取出用例
    if 'testcases' in include:
        # 每次for循环取出用例id
        for testcase_id in include.get('testcases'):
            # 取出用例的对象
            testcase_obj = Testcases.objects.filter(id=testcase_id).first()
            try:
                testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
            except Exception as e:
                # 如果前置用例报错了，则不管
                continue

            testcase_list.append(testcase_request)

    # 把当前需要执行的用例追加到testcase_list最后
    testcase_list.append(request)
    # 生成yaml：此时需要安装pyyaml
    # 将嵌套字典的列表转换为yaml文件
    with open(os.path.join(testcase_dir_path, instance.name + '.yaml'), 'w', encoding='utf-8') as f:
        # 生成yaml文件使用dump
        yaml.dump(testcase_list, f, allow_unicode=True)
        # 备注：all_unicode：允许使用unicode编码


def run_testcase(instance, testcase_dir_path):
    """运行用例"""
    # 1、运行用例：需要安装HttpRunner
    # 创建runner对象
    runner = HttpRunner()
    try:
        # 使用runner.run运行用例，传入目录testcase_dir_path
        runner.run(testcase_dir_path)
    except:
        res = {'ret': False, 'msg': '用例执行失败'}
        return Response(res, status=400)

    # 2、创建报告
    report_id = create_report(runner, instance.name)

    # 3、用例运行成功之后，需要把生成的报告id返回
    data = {
        'id': report_id
    }
    return Response(data, status=201)
