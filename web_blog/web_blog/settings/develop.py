from .base import *  # N0QA


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

# #接口的分页设置
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 2,
}

DEBUG = True

EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = "1531391246@qq.com"
EMAIL_HOST_PASSWORD = "gnewkzxalhlqbaba"
EMAIL_SUBJECT_PREFIX = "[django博客]"
SERVER_EMAIL = "1531391246@qq.com"
ADMINS = (('1531391246', '1531391246@qq.com'),)
