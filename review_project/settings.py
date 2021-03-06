"""
Django settings for review_project project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import logging.config
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT=os.path.join(BASE_DIR,'collectedstatic')

env_location=os.path.join(os.sep,'scratch','pyt3venvdjango2','.env')
load_dotenv(env_location)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^^v%_8uki#4h9k$yq=d@o8ycs@ww7v6h^-2p1ce&*cf16!&2j4'

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
    'configurations.apps.ConfigurationsConfig',
    'peer_review.apps.PeerReviewConfig',
    'peer_testing.apps.PeerTestingConfig',
    'manager_activities.apps.ManagerActivitiesConfig',
    'django_filters',
    'bootstrapform'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
]

ROOT_URLCONF = 'review_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates'),],
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

WSGI_APPLICATION = 'review_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': os.getenv('db_name'),
        'USER':os.getenv('db_user'),
        'PASSWORD':os.getenv('db_pass'),
        'HOST':os.getenv('db_host'),
        'PORT':os.getenv('db_port')
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
AUTH_USER_MODEL = 'configurations.User'


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS =[
    os.path.join(BASE_DIR,'static_files'),
]


LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    # Version of logging
    'disable_existing_loggers': False,
    'filters':{
        'simple':{
            '()':'configurations.HelperClasses.SystemLogFilter'
        }
    },
    'formatters':{
        'simple':{
            'format': '[ %(asctime)s - %(name)s ] - { %(levelname)s } ] : %(message)s \n',
            
        },
    },
    'handlers': {
        'fileDebug': {
            'level': 'DEBUG',
            'formatter': 'simple',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR,'app_logs','AppLogs','app-debug.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount':30,
            'filters':['simple']
        },
        'fileError': {
            'level': 'ERROR',
            'formatter': 'simple',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR,'app_logs','AppLogs','app-error.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount':30,
            'filters':['simple']
        },
        'djangoDebug': {
            'level': 'DEBUG',
            'formatter': 'simple',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR,'app_logs','DjangoLogs','djangoapp-debug.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount':30,
            'filters':['simple']
        },
    },
    'loggers': {
        '': {
            'handlers': ['fileError'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {
            'handlers': ['fileDebug'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django': {
            'handlers': ['djangoDebug'],
            'level': 'DEBUG',
            'propagate': True
        },
    },
}
logging.config.dictConfig(LOGGING)

