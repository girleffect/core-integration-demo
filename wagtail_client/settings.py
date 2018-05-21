"""
Django settings for wagtail_client project.

Generated by 'django-admin startproject' using Django 1.11.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.urls import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

SITE_CODE = os.environ.get('SITE_CODE', "none")

OIDC_STORE_ID_TOKEN = True  # Used by wagtail_client.utils.provider_logout_url()

OIDC_RP_CLIENT_ID = "unused"  # Some constructors require that this be set.
OIDC_RP_CLIENT_SECRET = "unused"  # some constructors require that this be set.
OIDC_OP = os.environ['OIDC_OP']
OIDC_AUTHENTICATE_CLASS = "wagtail_client.views.CustomAuthenticationRequestView"
OIDC_CALLBACK_CLASS = "wagtail_client.views.CustomAuthenticationCallbackView"

# The scopes that this application will request access to.
if SITE_CODE == "springster":
    OIDC_RP_SCOPES = 'openid profile site roles'
else:
    OIDC_RP_SCOPES = 'openid profile email address phone site roles'

# <URL of the OIDC OP authorization endpoint>
OIDC_OP_AUTHORIZATION_ENDPOINT = os.environ['OIDC_OP_AUTHORIZATION_ENDPOINT']

# <URL of the OIDC OP token endpoint>
OIDC_OP_TOKEN_ENDPOINT = os.environ['OIDC_OP_TOKEN_ENDPOINT']

# <URL of the OIDC OP userinfo endpoint>
OIDC_OP_USER_ENDPOINT = os.environ['OIDC_OP_USER_ENDPOINT']

# A method that will construct a logout URL for the Authentication Service.
# This is only required if the user needs to be logged out of the Authentication Service as well
# as this application.
OIDC_OP_LOGOUT_URL_METHOD = "wagtail_client.utils.provider_logout_url"

OIDC_OP_LOGOUT_URL = os.environ['OIDC_OP_LOGOUT_URL']

OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = 15 * 60  # 15 minutes

LOGIN_URL = reverse_lazy("login")
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# These can 404 for now, just so we know what got triggered.
LOGIN_REDIRECT_URL_FAILURE = reverse_lazy("login")  # "/failure/"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't(z+u(#qo@h+lgi)zp@7eu@tgtc@ij%g!jx9gfi%eu$(y4$t-k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# NOTE: DO NOT DO THIS FOR ANY PRODUCTION DJANGO.
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',

    'mozilla_django_oidc',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'wagtail_client',

    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',

    'modelcluster',
    'taggit',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
    # 'mozilla_django_oidc.middleware.SessionRefresh',
    'wagtail_client.middleware.CustomSessionRefresh'
]

ROOT_URLCONF = 'wagtail_client.urls'

AUTHENTICATION_BACKENDS = (
    'girleffect_oidc_integration.auth.GirlEffectOIDCBackend',
)

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

WSGI_APPLICATION = 'wagtail_client.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("DB_NAME", "wagtail"),
        "USER": os.environ.get("DB_USER", "wagtail"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "password"),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "CONN_MAX_AGE": 600
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'girleffect_oidc_integration': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'propagate': True,
        },
    },
}


@property
def TEST_ME():
    return "Foo"
