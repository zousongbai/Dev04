# -*- coding    : utf-8 -*-
# @Author       : С����
# @ProjectName  :Dev04
# @File         : handle_data.py
# @Time         : 2020/8/12 22:12

def handle_param_type(value):
    """
    �����������
    :param value: ����
    :return: value���ݵ�������
    """
    if isinstance(value,int):
        # ���value��int���ͣ���ǰ�Ĳ�����������Ϊint
        param_type = 'int'
    elif isinstance(value,float):
        param_type = 'float'
    elif isinstance(value,bool):
        param_type = 'boolean'
    else:
        param_type = 'string'
    return param_type



# ����validate������
def handle_data1(datas):
    """
    �����һ�����͵�����ת����
    ����˴����ݿ��ȡ�����ͣ�[{"check":"status_code","expected":200,"comparator":"equals"}]
    ת��Ϊǰ����Ҫ�����ͣ�[{"key": "status_code", "value": 200, "comparator": 'equals', "param_type": 'int'}]
    :param datas: ��ת���Ĳ����б�
    :return:
    """
    resulte_list = []
    # datas�����յ�����
    if datas is not None:
        # �ж�datas�Ƿ�Ϊ�գ���Ϊ�ղŽ���forѭ��
        for one_validate_dict in datas:
            # ��keyȡ��������ʵ�ʽ��
            key = one_validate_dict.get('check')
            # ��valueȡ���������������
            value = one_validate_dict.get('expected')
            # ���Ե�����
            comparator = one_validate_dict.get('comparator')

            # # ��Ҫ�Ĳ�������
            # if isinstance(value, int):
            #
            #     param_type = 'int'
            # elif isinstance(value,bool):
            #     # ���value��bool���ͣ���ǰ�Ĳ�����������Ϊboolean
            #     param_type = 'boolean'
            # else:
            #     # �������ͣ�������Ϊstring
            #     param_type = 'string'

            one_dict={
                'key':key,
                'value':value,
                'comparator':comparator,
                'param_type':handle_param_type(value)
            }
            # ���ֵ�one_dict�ŵ��б�����
            resulte_list.append(one_dict)
    # resulte_list��ǰ����Ҫ������
    return resulte_list
