import os
import dj_database_url
from pythonjsonlogger import jsonlogger

PROJECT_NAME = 'digests'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
SECRET_KEY = os.environ.get('APP_SECRET', 'secret')

ENVIRONMENT = os.environ.get('ENVIRONMENT_NAME', 'dev')
DEBUG = bool(os.environ.get('DEBUG', 0))
DEFAULT_LOG_DIR = '/srv/digests/var/logs'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'core',
    'digests',
]

MIDDLEWARE = [
    'core.middleware.kong_authentication',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    # looks for `DATABASE_URL` env var
    # e.g. DATABASE_URL=postgres://user:password@db:5432/digests
    'default': dj_database_url.config(),
}

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

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_PARSER_CLASSES': (
        'digests.parsers.DigestParser',
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'digests.renderers.DigestRenderer',
        'digests.renderers.DigestsRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'DATETIME_FORMAT': "%Y-%m-%dT%H:%M:%SZ",
}

LOG_ATTRS = ['asctime', 'created', 'levelname', 'message',
             'filename', 'funcName', 'lineno', 'module', 'pathname']
LOG_FORMAT_STR = ' '.join(['%(' + v + ')s' for v in LOG_ATTRS])

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': jsonlogger.JsonFormatter,
            'format': LOG_FORMAT_STR,
        },
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%b-%dT%H:%M:%SZ"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(DEFAULT_LOG_DIR, '%s.json.log' % PROJECT_NAME),
            'formatter': 'json'
        },
        'console': {
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'core': {
            'handlers': ['file'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'digests': {
            'handlers': ['file'],
            'propagate': False,
            'level': 'DEBUG',
        }
    },
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

CONSUMER_GROUPS_HEADER = 'HTTP_X_CONSUMER_GROUPS'
AUTHORIZATION_PREVIEW_HEADER = 'Digests-Can-Preview'
AUTHORIZATION_MODIFICATION_HEADER = 'Digests-Can-Modify'

DIGEST_CONTENT_TYPE = 'application/vnd.elife.digest+json;version=1'
DIGESTS_CONTENT_TYPE = 'application/vnd.elife.digest-list+json;version=1'
ERROR_CONTENT_TYPE = 'application/problem+json'
