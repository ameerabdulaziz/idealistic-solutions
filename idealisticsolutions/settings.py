# Import below line for celery, It should be in first line
from __future__ import absolute_import, unicode_literals

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['test.idealisticsolutions.com','127.0.0.1']
# ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'api',
    'bootstrap4',
    'ckeditor',
    'ckeditor_uploader',
    'django_celery_results',
    'crispy_forms',
    # 'django_celery_beat',
    'paypal.standard.ipn',
    'rest_framework',
    'stripe',
    # 'debug_toolbar',

    'accounts',
    'carts',
    'orders',
    'search',
    'shop',
    'ticketing_system',
    'static_pages',
    'sms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'idealisticsolutions.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.shop_links',
                'carts.context_processors.cart_items_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'idealisticsolutions.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('ENGINE'),
        'NAME': os.environ.get('NAME'),
        'USER': os.environ.get('USER'),
        'PASSWORD': os.environ.get('PASSWORD'),
        'HOST': os.environ.get('HOST'),
        'port': os.environ.get('port'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATICFILES_DIRS = [STATIC_DIR, ]
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles', 'static_root')
if not DEBUG:
	STATIC_ROOT = '/home/idealisticsolutions/domains/test.idealisticsolutions.com/public_html/idealisticsolutions/static/'


MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_DIR

"""
    >>>>> MESSAGES <<<<<
"""
from django.contrib.messages import constants

MESSAGE_TAGS = {
    constants.ERROR: 'danger'
}

"""
    >>>>> CKEDITOR CONFIGURATION <<<<<
"""
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}

"""
    >>>>> REDIRECT URLS AFTER LOGIN & LOGOUT <<<<<
"""
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

"""
    >>>>> CELERY SETTINGS <<<<<
"""
CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'
#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
# To save results in database
CELERY_RESULT_BACKEND = 'django-db'
# For the cache backend you can use:
# CELERY_RESULT_BACKEND = 'django-cache'
CELERY_TASK_SERIALIZER = 'json'

"""
    >>>>> REST FRAMEWORK <<<<<
"""
REST_FRAMEWORK = {
    # TO disable all api from guest and all user have to login to see them
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    # To activate JWT in api
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
}

# Settings --> Some of Simple JWT's behavior can be customized through settings variables in settings.py:
from datetime import timedelta

SIMPLE_JWT = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    # 'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # 'ROTATE_REFRESH_TOKENS': False,
    # 'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    # TO use Django key as toke key for more security
    # 'SIGNING_KEY': settings.SECRET_KEY,
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    # 'AUTH_HEADER_TYPES': ('Bearer',),
    # 'USER_ID_FIELD': 'id',
    # 'USER_ID_CLAIM': 'user_id',
    #
    # 'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    # 'TOKEN_TYPE_CLAIM': 'token_type',
    #
    # 'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    # 'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    # 'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

"""
    >>>>> PAYMENT METHODS <<<<<
"""
# Stripe
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
# Paypal
PAYPAL_RECEIVER_EMAIL = os.environ.get('PAYPAL_RECEIVER_EMAIL')
PAYPAL_TEST = True

"""
    >>>>> MAILING CONFIGURATION <<<<<
"""
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT =  os.environ.get('EMAIL_PORT')

# debug_toolbar
INTERNAL_IPS = ['127.0.0.1', '108.30.141.250', '192.168.1.1', '192.168.1.101']

# twilio Settings
twilio_from_ = "+13477718768"
# Your Account SID from twilio.com/console
twilio_account_sid = "AC73496b96f66d773f6a650c5f250af4ad"
# Your Auth Token from twilio.com/console
twilio_auth_token = "96ed19ed53c786f466687093d557641b"


CRISPY_TEMPLATE_PACK = 'bootstrap3'
