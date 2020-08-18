"""
Django settings for Dev04 project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import os
import sys
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 把某个路径添加到系统模块搜索路径中去
# sys.path为一个列表
sys.path.append(os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@(35-t#w!nxzp3nuky6$8xl2fch*i!-sgk_omj4n(bpszg_7r@'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# 需要关掉调试功能
DEBUG = False


# 可以使用哪些IP或者域名来访问系统
# 默认为空，可以使用127.0.0.1或者localhost
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'drf_yasg',

    # 注册子应用
    # 格式：子应用名.apps.子应用名首字母大写Config，除了子应用名外，其他会自动提示
    'projects',
    'interfaces',  # 注册子应用，可以直接使用子应用名
    'user',
    'testcases',
    'configures',
    'envs',
    'debugtalks',
    'reports',
    'testsuits',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 需要添加在CommonMiddleware中间件之前
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# ①CORS_ORIGIN_ALLOW_ALL为True，指定所有域名（IP）都可以访问后端接口，默认为False
CORS_ORIGIN_ALLOW_ALL=True

# # ②如果CORS_ORIGIN_ALLOW_ALL为False，则需要CORS_ORIGIN_WHITELIST指定能够访问后端接口的IP或域名列表
# CORS_ORIGIN_WHITELIST=[
#     'http://127.0.0.1:8080',
#     'http://localhost:8080',
#     'http://192.168.1.63:8080',
#     'http://127.0.0.1:9000',
#     'http://localhost:9000',
# ]
# 允许跨域时携带cookie，设置为True，默认为False　
CORS_ALLOW_CREDENIALS=True


ROOT_URLCONF = 'Dev04.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # APP_DIRS：设为True的意思是查找模板可以去子应用下面去查找
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Dev04.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# 需要在全局settings.py中的DATABASES字典中来配置数据库的信息
DATABASES = {
    # 在Django中数据库的标识
    'default': {
        # 指定数据库使用的引擎
        'ENGINE': 'django.db.backends.mysql',
        # 指定数据库的名称
        'NAME': 'dev04_dj',
        # 指定连接的数据库主机地址：域名和IP都可以
        'HOST': 'localhost',
        # 指定数据库的连接端口号：默认3306
        'PORT': 3306,
        #  指定用户名
        'USER': 'root',
        #   数据库密码
        'PASSWORD': '123456'
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# 指定简体中文
LANGUAGE_CODE = 'zh-hans'

# 指定简体中文
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# 在全局配置文件setting.py文件中的REST_FRAMEWORK字典里修改DRF框架的配置
REST_FRAMEWORK = {
    # 'NON_FIELD_ERRORS_KEY': 'errors',
    # (1)可以修改默认的渲染类（处理符合的数据形式）
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # 默认返回json
        'rest_framework.renderers.BrowsableAPIRenderer',  # 返回HTML页面
    ],
    # 指定过滤引擎
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.backends.DjangoFilterBackend',  # 指定过滤引擎
        'rest_framework.filters.OrderingFilter',  # 指定排序引擎
    ],
    # 需要指定分页引擎，可以使用默认的PageNumberPagination分页引擎类
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

    # 指定自定义的引擎类
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.MyPagination',
    # 必须指定每一页的数据条数
    'PAGE_SIZE': 3,

    # 指定用于支持coreapi的Schema
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

    # DEFAULT_AUTHENTICATION_CLASSES：指定默认的认证类（认证方式）
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 指定使用JWT token认证方式，即jsonwebtoken认证
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',

        # 会话认证
        'rest_framework.authentication.SessionAuthentication',
        # 基本认证（用户名和密码认证），在测试或开发环境使用，生成环境不用
        'rest_framework.authentication.BasicAuthentication',

    ],

    # DEFAULT_PERMISSION_CLASSES：指定认证之后，能获取到的权限
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     # ①AllowAny：不需要登录就有任意权限，只要登录之后，就具备任意权限
    #     'rest_framework.permissions.AllowAny',
    #     # ②IsAuthenticated：只要登录之后，就具体任务权限
    #     # 'rest_framework.permissions.IsAuthenticated',
    #     # ③IsAdminUser：指定，只有为管理员用户才有任意权限
    #     # 'rest_framework.permissions.IsAdminUser',
    #     # ④IsAuthenticatedOrReadOnly：指定如果没有登录，只能获取数据；如果登录成功就具备任意权限
    #     # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    # ],
}

# 可以在全局配置settings.py中的LOGGING，来配置日志信息
LOGGING = {
    # 版本号
    'version': 1,
    # 指定是否禁用已经存在的日志器
    'disable_existing_loggers': False,
    # 日志的显示格式
    'formatters': {
        # simple为简化版格式的日志
        'simple': {
            'format': '%(asctime)s - [%(levelname)s] - [msg]%(message)s'
        },
        # verbose为详细格式的日志
        'verbose': {
            'format': '%(asctime)s - [%(levelname)s] - %(name)s - [msg]%(message)s - [%(filename)s:%(lineno)d ]'
            # filename：哪个文件出现的日志
            # lineno：哪一行出现的日志，即打印出抛出日志的文件名和哪一行打印出来
        },
    },
    # filters指定日志过滤器
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # handlers指定日志输出渠道
    'handlers': {
        # console指定输出到控制台
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # 日志保存到日志文件
        'file': {
            'level': 'DEBUG',
            # RotatingFileHandler：轮转的日志输出渠道
            'class': 'logging.handlers.RotatingFileHandler',
            # 指定存放日志文件的所处路径
            'filename': os.path.join(BASE_DIR, "logs/test.text"),  # 日志文件的位置
            # 备注：BASE_DIR：项目工程
            # 一个日志文件最大存放多大字节：如设置100M
            'maxBytes': 100 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding':'utf-8'
        },
    },
    # 定义日志器
    'loggers': {
        'mytest': {  # 定义了一个名为mytest的日志器
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'DEBUG',  # 日志器接收的最低日志级别
        },
    }
}

# # 默认使用的是Django auth子应用下的User模型类
# # 可以指定自定义的模型类
# AUTH_USER_MODEL = 'auth.User'

# User模型类中有很多字段，其中有一个is_staff字段，指定是否为超级管理员。如果未0，则为普通用户；如果为1，则为超级管理员
# 可以在命令行下使用python manage.py createsuperuser，来创建超级管理员

# 在全局配置JWT_AUTH中，可以覆盖JWT相关的参数
JWT_AUTH = {
    # 指定处理登录接口响应数据的函数
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'utils.jwt_handle.jwt_response_payload_handler',
    # 前端用户访问一些需要认证之后的接口，那么默认需要在请求头中携带参数，
    # 请求key为Authorization，值为前缀+空格+token值，如：JWT xxxjjgkhg

    # 可以指定token过期时间，默认为5分钟
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    #  days=1：一天后到期

    # 指定前端传递token值得前缀
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

# 测试报告存放目录
# 在全局配置文件settings.py文件中定义变量，变量名要大写
# django.conf.setting
REPORT_DIR = os.path.join(BASE_DIR,'reports')
SUITES_DIR = os.path.join(BASE_DIR, 'suites')
# 收集静态文件
STATIC_ROOT=os.path.join(BASE_DIR, 'static')


