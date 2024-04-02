import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# load django secret key
from dotenv import load_dotenv
load_dotenv()
djagno_secret_key = os.environ.get('SECRET_KEY')
SECRET_KEY = djagno_secret_key


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
if DEBUG:
    ALLOWED_HOSTS = ["*"]
    SECURE_SSL_REDIRECT = False
else:
    ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.result",  # project apps
    'sslserver',  # test https
]

if DEBUG:
    # for python manage.py runserver
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",           #
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",               #
        "django.contrib.auth.middleware.AuthenticationMiddleware", #
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ]
else:
    # for gunicorn / it doesn't work django runserver
    MIDDLEWARE = [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ]

ROOT_URLCONF = "nearshoku.urls"

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],  # set up template basedir
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

WSGI_APPLICATION = "nearshoku.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
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
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
import whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400