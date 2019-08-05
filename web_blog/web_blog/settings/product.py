#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2019/8/5 10:24
# @Author : Tan 
# @Email : 1531391246@qq.com
# @File : product.py
# @Software: PyCharm
from .base import *  # NOQA
import os

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += ('mdeditor', )

LOGIN_URL = '/login/'

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# 文件上传的路径
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# 文件存储方式
DEFAULT_FILE_STORAGE = 'web_blog.storage.WatermarkStorage'

# 数据库配置
DATABASES_PASSWORD = os.environ['DATABASES_PASSWORD']
DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'web_blog',
        'USER': 'root',
        'PASSWORD': DATABASES_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'CONN_MAX_AGE': 60,
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}
# 缓存配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "PARSER_CLASS": "redis.connection.HiredisParser",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
        }
    }
}

# 邮箱配置
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = "1531391246@qq.com"
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_SUBJECT_PREFIX = "[django博客]"
SERVER_EMAIL = "1531391246@qq.com"
DEFAULT_FROM_EMAIL = "1531391246@qq.com"
ADMINS = MANAGERS = [('admin', '1531391246@qq.com'), ]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# 日志处理
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
      'default': {
          'format': '%(levelname)s %(asctime)s %(module)s:%(funcName)s:%(lineno)d %(message)s'
      }
    },
    'handlers': {
        'console': {
          'level': 'INFO',
          'class': 'logging.StreamHandler',
          'formatter': 'default',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/path/to/django/debug.log',
            'format': 'default',
            'maxBytes': 1024 * 1024,
            'backupCount': 5,
        },
        'mail_admin': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['special'],
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
"""gnewkzxalhlqbaba"""
