# -*- coding    : utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : handle_data.py
# @Time         : 2020/8/12 22:12

def handle_param_type(value):
    """
    处理参数类型
    :param value: 数据
    :return: value数据的类型名
    """
    if isinstance(value,int):
        # 如果value是int类型，则当前的参数类型设置为int
        param_type = 'int'
    elif isinstance(value,float):
        param_type = 'float'
    elif isinstance(value,bool):
        param_type = 'boolean'
    else:
        param_type = 'string'
    return param_type



# 处理validate参数：
def handle_data1(datas):
    """
    处理第一种类型的数据转化：
    将后端从数据库读取的类型：[{"check":"status_code","expected":200,"comparator":"equals"}]
    转化为前端需要的类型：[{"key": "status_code", "value": 200, "comparator": 'equals', "param_type": 'int'}]
    :param datas: 待转换的参数列表
    :return:
    """
    resulte_list = []
    # datas：接收的数据
    if datas is not None:
        # 判断datas是否为空，不为空才进行for循环
        for one_validate_dict in datas:
            # 将key取出来，即实际结果
            key = one_validate_dict.get('check')
            # 将value取出来，即期望结果
            value = one_validate_dict.get('expected')
            # 断言的类型
            comparator = one_validate_dict.get('comparator')

            # # 需要的参数类型
            # if isinstance(value, int):
            #
            #     param_type = 'int'
            # elif isinstance(value,bool):
            #     # 如果value是bool类型，则当前的参数类型设置为boolean
            #     param_type = 'boolean'
            # else:
            #     # 其他类型，则设置为string
            #     param_type = 'string'

            one_dict={
                'key':key,
                'value':value,
                'comparator':comparator,
                'param_type':handle_param_type(value)
            }
            # 将字典one_dict放到列表里面
            resulte_list.append(one_dict)
    # resulte_list：前端需要的数据
    return resulte_list
