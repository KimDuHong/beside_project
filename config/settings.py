"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
import os
import environ

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

THIRD_PARTY_APPS = [
    "corsheaders",
    "drf_yasg",
    "rest_framework",
    "debug_toolbar",
]
CUSTOM_APPS = [
    "users.apps.UsersConfig",
    "memes.apps.MemesConfig",
    "tags.apps.TagsConfig",
]

SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = SYSTEM_APPS + CUSTOM_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
# INTERNAL_IPS = ["127.0.0.1"]
if DEBUG:
    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/


LANGUAGE_CODE = "ko-KR"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = "/static/file/"

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SERVER = os.environ.get("SERVER", False)

if SERVER:
    sentry_sdk.init(
        dsn="https://84d3956dc436b6d24b0c859eedbb6326@o4504859857387520.ingest.sentry.io/4505640866021376",
        integrations=[
            DjangoIntegration(
                transaction_style="url",
            )
        ],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

NCP_ACCESS_KEY = os.environ.get("NCP_ACCESS_KEY")
NCP_SECRET_KEY = os.environ.get("NCP_SECRET_KEY")

if SERVER == "Prod":
    NAVER_CLIENT_ID = os.environ.get("PROD_NAVER_CLLIENT_ID")
    KAKAO_CLIENT_ID = os.environ.get("PROD_KAKAO_CLLIENT_ID")

    NAVER_REDIRECT_URI = os.environ.get("PROD_NAVER_REDIRECT_URI")
    KAKAO_REDIRECT_URI = os.environ.get("PROD_KAKAO_REDIRECT_URI")

    NAVER_CLIENT_SECRET = os.environ.get("PROD_NAVER_CLIENT_SECRET")
else:
    NAVER_CLIENT_ID = os.environ.get("DEV_NAVER_CLLIENT_ID")
    KAKAO_CLIENT_ID = os.environ.get("DEV_KAKAO_CLLIENT_ID")

    NAVER_REDIRECT_URI = os.environ.get("DEV_NAVER_REDIRECT_URI")
    KAKAO_REDIRECT_URI = os.environ.get("DEV_KAKAO_REDIRECT_URI")

    NAVER_CLIENT_SECRET = os.environ.get("DEV_NAVER_CLIENT_SECRET")
