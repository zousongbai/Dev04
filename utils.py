# -*- coding    : utf-8 -*-
# @Author       : 小青年
# @ProjectName  :Dev04
# @File         : utils.py
# @Time         : 2020/7/9 23:00

# 导入locale
import locale  # locale：专门处理编码
# 将本地的语言设置为chinese
locale.setlocale(locale.LC_CTYPE,'chinese')
# 格式化字符串
datetime_fmt='%Y年%m月%d日 %H:%M:%S'