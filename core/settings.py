import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True
ALLOWED_HOSTS = ['*']
SECRET_KEY = 'django-insecure-rem!wy@4l_e5yh&w3)bshowiu_hz&obw4@$s%7k#0_fp&hgokj'

static_root = 'attend/static'
media_root = os.path.join(BASE_DIR, 'media')


INSTALLED_APPS = [
    'attend',
    'django_filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
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
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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


IPWARE_META_PRECEDENCE_ORDER = (
  "X_FORWARDED_FOR",  # AWS ELB (default client is `left-most` [`<client>, <proxy1>, <proxy2>`])
  "HTTP_X_FORWARDED_FOR",  # Similar to X_FORWARDED_TO
  "HTTP_CLIENT_IP",  # Standard headers used by providers such as Amazon EC2, Heroku etc.
  "HTTP_X_REAL_IP",  # Standard headers used by providers such as Amazon EC2, Heroku etc.
  "HTTP_X_FORWARDED",  # Squid and others
  "HTTP_X_CLUSTER_CLIENT_IP",  # Rackspace LB and Riverbed Stingray
  "HTTP_FORWARDED_FOR",  # RFC 7239
  "HTTP_FORWARDED",  # RFC 7239
  "HTTP_VIA",  # Squid and others
  "X-CLIENT-IP",  # Microsoft Azure
  "X-REAL-IP",  # NGINX
  "X-CLUSTER-CLIENT-IP",  # Rackspace Cloud Load Balancers
  "X_FORWARDED",  # Squid
  "FORWARDED_FOR",  # RFC 7239
  "CF-CONNECTING-IP",  # CloudFlare
  "TRUE-CLIENT-IP",  # CloudFlare Enterprise,
  "FASTLY-CLIENT-IP",  # Firebase, Fastly
  "FORWARDED",  # RFC 7239
  "CLIENT-IP",  # Akamai and Cloudflare: True-Client-IP and Fastly: Fastly-Client-IP
  "REMOTE_ADDR",  # Default
)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Etc/GMT-3'
# TIME_ZONE = 'Africa/Cairo'

USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = static_root

MEDIA_URL = '/media/'
MEDIA_ROOT = media_root


AUTH_USER_MODEL = 'attend.User'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


