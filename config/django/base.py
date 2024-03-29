import os
from config.env import env, BASE_DIR

env.read_env(os.path.join(BASE_DIR, ".env"))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_shop.config')
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=ug_ucl@yi6^mrcjyz%(u0%&g2adt#bz3@yos%#@*t#t!ypx=a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


# Application definition
LOCAL_APPS = [
    'django_shop.core.apps.CoreConfig',
    'django_shop.common.apps.CommonConfig',
    'django_shop.django_phone_login.apps.DjangoPhoneLoginConfig',
    'django_shop.products.apps.ProductsConfig',
    'django_shop.categories.apps.CategoriesConfig',
    'django_shop.coupon.apps.CouponConfig',
    'django_shop.order.apps.OrderConfig',
    'django_shop.user_profile.apps.UserProfileConfig',
    'django_shop.rate.apps.RateConfig',
    'django_shop.cart.apps.CartConfig',

]

THIRD_PARTY_APPS = [
    'rest_framework',
    'django_filters',
    'django_celery_results',
    'django_celery_beat',
    'corsheaders',
    'drf_spectacular',
    'django_extensions',
    'widget_tweaks',
    'django_comments',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_shop.django_phone_login.middleware.IpAddressMiddleware'
]

ROOT_URLCONF = 'config.urls'

AUTHENTICATION_BACKENDS = [
    'django_shop.django_phone_login.backend.phone_backend.PhoneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': env.db('DATABASE_URL', default='psql://user:password@127.0.0.1:5432/django_shop'),
# }
# DATABASES['default']['ATOMIC_REQUESTS'] = True
#
# if os.environ.get('GITHUB_WORKFLOW'):
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': 'github_actions',
#             'USER': 'user',
#             'PASSWORD': 'password',
#             'HOST': '127.0.0.1',
#             'PORT': '5432',
#         }
#     }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':os.path.join(BASE_DIR ,'db.sqlite3'),
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
AUTH_USER_MODEL = 'django_phone_login.User'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'django_shop.api.exception_handlers.drf_default_with_modifications_exception_handler',
    # 'EXCEPTION_HANDLER': 'django_shop.api.exception_handlers.hacksoft_proposed_exception_handler',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}


# Redis
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': env("REDIS_LOCATION", default="redis://localhost:6379"),
#     }
# }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15


APP_DOMAIN = env("APP_DOMAIN", default="http://localhost:8000")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CART_SESSION_ID = 'cart'

from config.settings.cors import *  # noqa
# from config.settings.jwt import *  # noqa
from config.settings.sessions import *  # noqa
# from config.settings.celery import *  # noqa
from config.settings.swagger import *  # noqa
#from config.settings.sentry import *  # noqa
#from config.settings.email_sending import *  # noqa