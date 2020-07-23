# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : jwt_handle.py
# @Time         : 2020/7/23 17:57

def jwt_response_payload_handler(token, user=None, request=None):

    return {
        'user_id':user.id,
        'username':user.username,
        'token': token
    }
