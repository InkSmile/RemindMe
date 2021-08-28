"""
Django settings for Reminder project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import datetime
import os
import environs
from pathlib import Path

env = environs.Env()
env.read_env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', 'test')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG_MODE', True)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # New apps
    'authentication',
    'notifications',
    'user_profile',
    'rest_framework',
    'corsheaders',
    'reminders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    "corsheaders.middleware.CorsMiddleware",

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Reminder.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'Reminder.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str("POSTGRES_DB", "django_db"),
        'USER': env.str("POSTGRES_USER", "user"),
        'PASSWORD': env.str("POSTGRES_PASSWORD", "password"),
        'HOST': env.str("DB_HOST", "localhost"),
        'PORT': env.str("DB_PORT", "5433"),
    }
}



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': env.str("POSTGRES_DB"),
#         'USER': env.str("POSTGRES_USER"),
#         'PASSWORD': env.str("POSTGRES_PASSWORD"),
#         'HOST': env.str("DB_HOST"),
#         'PORT': env.str("DB_PORT"),
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'authentication.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'JSON_UNDERSCOREIZE': {
        'no_underscore_before_number': True,
    },
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(
        hours=env.int('ACCESS_TOKEN_LIFETIME_HOURS', 100),
        minutes=env.int('ACCESS_TOKEN_LIFETIME_MINUTES', 0),
    ),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=env.int('REFRESH_TOKEN_LIFETIME_DAYS', 7)),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': True,
    'VERIFY_EXPIRATION': True,

    'AUTH_HEADER_TYPES': ('JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}


FE_SITE_URL = env.str('FE_SITE_URL', '')

# Celery Settings
CELERY_BROKER_URL = env.str('BROKER_URL', '')
CELERY_TASK_DEFAULT_QUEUE = "django"
CELERY_TASK_SOFT_TIME_LIMIT = env.int('TASK_SOFT_TIME_LIMIT_SEC', 40)

# MailJet Settings
MAILJET_PUBLIC_KEY = env.str('MAILJET_PUBLIC_KEY', '')
MAILJET_SECRET_KEY = env.str('MAILJET_SECRET_KEY', '')
MAILJET_USER = env.str('MAILJET_USER', '')

USER_ACTIVATION_URL = env.str('USER_ACTIVATION_URL', '')

# EMAIL_BACKEND = 'django_mailjet.backends.MailjetBackend'