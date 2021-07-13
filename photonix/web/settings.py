"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

from datetime import timedelta
import os
from pathlib import Path

from .utils import get_secret_key


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = str(Path(__file__).parent.parent.resolve())

SECRET_KEY = get_secret_key()

DEBUG = os.environ.get('ENV', 'prd') != 'prd'

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS', 'localhost,127.0.0.1,[::1]').split(',')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',
    'corsheaders',
    'photonix.common',
    'photonix.accounts',
    'photonix.photos',
    'photonix.web',
    'graphene_django',
    'django_filters',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'photonix.web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'photonix.web.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'HOST':     os.environ.get('POSTGRES_HOST', '127.0.0.1'),
        'NAME':     os.environ.get('POSTGRES_DB', 'photonix'),
        'USER':     os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'password'),
        'PORT':     int(os.environ.get('POSTGRES_PORT', '5432')),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'color': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(asctime)s %(levelname)-8s %(message)s',
            'log_colors': {
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'white,bg_red',
            },
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'color',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
            'propagate': False,
        },
        'photonix': {
            'handlers': ['console'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'accounts.User'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


if os.path.exists('/data'):
    DATA_DIR = str(Path('/data'))
else:
    DATA_DIR = str(Path(BASE_DIR).parent / 'data')

CACHE_DIR = str(Path(DATA_DIR) / 'cache')
MODEL_DIR = str(Path(DATA_DIR) / 'models')

STATIC_ROOT = '/srv/static-collected'
STATIC_URL = '/static-collected/'

MEDIA_ROOT = str(Path(BASE_DIR).parent / 'data')

THUMBNAIL_ROOT = str(Path(CACHE_DIR) / 'thumbnails')
THUMBNAIL_URL = '/thumbnails/'

THUMBNAIL_SIZES = [
    # Width, height, crop method, JPEG quality, whether it should be generated upon upload, force accurate gamma-aware sRGB resizing
    (256, 256, 'cover', 50, True, True),  # Square thumbnails
    # We use the largest dimension for both dimensions as they won't crop and some with in portrait mode
    # (960, 960, 'contain', 75, False, False),  # 960px
    # (1920, 1920, 'contain', 75, False, False),  # 2k
    (3840, 3840, 'contain', 75, False, False),  # 4k
]


PHOTO_INPUT_DIRS = [str(Path(BASE_DIR).parent.parent / 'photos_to_import')]
PHOTO_OUTPUT_DIRS = [
    {
        'EXTENSIONS': ['jpg', 'jpeg', 'mov', 'mp4', 'm4v', '3gp'],
        'PATH': '/data/photos',
    },
    {
        'EXTENSIONS': ['cr2'],
        'PATH': '/data/raw-photos',
    },
]
PHOTO_RAW_PROCESSED_DIR = '/data/raw-photos-processed'

MODEL_INFO_URL = 'https://photonix.org/models.json'

GRAPHENE = {
    'SCHEMA': 'photonix.web.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
    'JWT_EXPIRATION_DELTA': timedelta(minutes=15),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=365),
}

APPEND_SLASHES = False

CORS_ORIGIN_WHITELIST = []
