# -*- coding:utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : test_jwt.py
# @Time         : 2020/7/23 15:25

import jwt

# 第一部分的header，一般不需要指定，有默认值
# 第二部分的payload：可以指定后端需要存放的一些非敏感的信息
# 载荷
payload={
    'username':'小李',
    'age':18,
}

# 服务端创建token令牌的过程
token=jwt.encode(payload,key='666')
# 备注：key：加密，加盐处
print(token)

# 服务端对前端用户传递的token进行解密过程
one_var=jwt.decode(token,key='666')
print(one_var)