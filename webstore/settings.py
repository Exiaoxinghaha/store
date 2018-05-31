"""
Django settings for webstore project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#%tbyr$2&-g$)jo@+o-*2rqm%7c8p60i$y73t3ll*)csdtztx&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'shop',
    'shopcart',
    'shoporder',
    'haystack',
    'tinymce',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shopcart.middleware.ShopCartSetSessionMiddleware',
]

ROOT_URLCONF = 'webstore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'shop.content_processors.categorys',
                'shopcart.content_processors.goods_num',
            ],
        },
    },
]

WSGI_APPLICATION = 'webstore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'webstore',
        'HOST': '192.168.43.107',
        'PORT': 3306,
        'USER': 'guoxing',
        'PASSWORD': 'qwe123'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)

MEDIA_URL = '/static/images/'
MEDIA_ROOT = (
    os.path.join(BASE_DIR,'static/images')
)

# 指定使用auth组件的model
AUTH_USER_MODEL = 'account.UserProfile'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = '18639756226@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'qwe123'
# 收件人看到的发件人
EMAIL_FROM = 'store <18639756226@163.com>'  # 需要和邮箱号码一致

LOGIN_URL = '/account/login/'

# 配置缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",  # redis的ip地址
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",  # 使用redis默认的缓存
        }
    }
}

# 搜索引擎
HAYSTACK_CONNECTIONS = {
     'default': {
            'ENGINE': 'utils.whoosh_zh_backend.WhooshEngine',      #该引擎为英文搜索引擎，后面会讲怎么修改为支持中文
            'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        },
    }
# 每次搜索展示的数据
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 15

# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 配置富文本编辑器
TINYMCE_DEFAULT_CONFIG = {
    "height": 600,
    "width": 400,
    "theme": "advanced",
    "preview_styles": True
}

STATIC_ROOT = "/tmp/collectstatic"