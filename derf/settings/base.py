"""
Django settings for derf project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
from urllib.parse import quote

import environ
from celery.schedules import crontab


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# Build paths inside the project like this: os.path.join(SITE_ROOT, ...)
SITE_ROOT = os.path.dirname(os.path.dirname(__file__))

# Load env to get settings
env = environ.Env()

# Set to true during docker image building (e.g. when running collectstatic)
IS_DOCKER_BUILD = env.bool("DJANGO_DOCKER_BUILD", default=False)

PROJECT_NAME = "derf"
# Shown in error pages and some other places
PROJECT_TITLE = "derf"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=True)

ADMINS = (("Admins", "fred.eric.kirsi@gmail.com"),)
MANAGERS = ADMINS
EMAIL_SUBJECT_PREFIX = "[derf] "  # subject prefix for managers & admins

SESSION_COOKIE_NAME = f"{PROJECT_NAME}_ssid"
SESSION_COOKIE_DOMAIN = env.str("DJANGO_SESSION_COOKIE_DOMAIN", default=None)

INSTALLED_APPS = [
    # Local apps
    "accounts",
    PROJECT_NAME,
    # Third-party apps
    "django_js_reverse",
    "webpack_loader",
    "crispy_forms",
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(SITE_ROOT, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django_settings_export.settings_export",
            ],
        },
    },
]

# Database
DATABASES = {
    # When using DJANGO_DATABASE_URL, unsafe characters in the url should be encoded.
    # See: https://django-environ.readthedocs.io/en/latest/#using-unsafe-characters-in-urls
    "default": env.db_url(
        "DJANGO_DATABASE_URL",
        default="psql://{user}:{password}@{host}:{port}/{name}?sslmode={sslmode}".format(
            host=env.str("DJANGO_DATABASE_HOST", default="postgres"),
            port=env.int("DJANGO_DATABASE_PORT", default=5432),
            name=quote(env.str("DJANGO_DATABASE_NAME", default="derf")),
            user=quote(env.str("DJANGO_DATABASE_USER", default="derf")),
            password=quote(
                env.str("DJANGO_DATABASE_PASSWORD", default="derf"),
            ),
            sslmode=env.str("DJANGO_DATABASE_SSLMODE", default="disable"),
        ),
    )
}


# Redis config (used for caching and celery)
REDIS_URL = env.str("DJANGO_REDIS_URL", default="redis://redis:6379/1")
REDIS_CACHE_URL = env.str("DJANGO_REDIS_CACHE_URL", default=REDIS_URL)
REDIS_CELERY_URL = env.str("DJANGO_REDIS_CELERY_URL", default=REDIS_URL)
# Set your Celerybeat tasks/schedule here
# Rest of Celery configuration lives in celery_settings.py
CELERYBEAT_SCHEDULE = {
    "default-task": {
        # TODO: Remove the default task after confirming that Celery works.
        "task": "derf.tasks.default_task",
        "schedule": 5 * 60,
    },
    "cleanup-old-sessions": {
        "task": "derf.tasks.cleanup_old_sessions",
        # TODO define the best time suitable for the cleanup.
        "schedule": crontab(minute=45, hour=2),
    },
}


# Caching
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CACHE_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}


# Internationalization
LANGUAGE_CODE = "en"
LANGUAGES = (
    ("en", "English"),
    ("et", "Eesti keel"),
)
LOCALE_PATHS = ("locale",)

TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Media files (user uploaded/site generated)
MEDIA_ROOT = env.str("DJANGO_MEDIA_ROOT", default="/files/media")
MEDIA_URL = env.str("DJANGO_MEDIA_URL", default="/media/")
MEDIAFILES_LOCATION = env.str("DJANGO_MEDIAFILES_LOCATION", default="media")

# In staging/prod we use S3 for file storage engine
AWS_ACCESS_KEY_ID = "<unset>"
AWS_SECRET_ACCESS_KEY = "<unset>"
AWS_STORAGE_BUCKET_NAME = "<unset>"
AWS_DEFAULT_ACL = "public-read"
AWS_IS_GZIPPED = True
AWS_S3_FILE_OVERWRITE = False
AWS_S3_REGION_NAME = "eu-central-1"
AWS_S3_SIGNATURE_VERSION = "s3v4"

# Only set DJANGO_AWS_S3_ENDPOINT_URL if it's defined in environment, fallback to default value in other cases
# Useful for s3 provided by other parties than AWS, like DO.
if env.str("DJANGO_AWS_S3_ENDPOINT_URL", default=""):
    AWS_S3_ENDPOINT_URL = env.str("DJANGO_AWS_S3_ENDPOINT_URL")

# Should be True unless using s3 provider that doesn't support it (like DO)
AWS_S3_ENCRYPTION = env.bool("DJANGO_AWS_S3_ENCRYPTION", default=True)

# This helps get around a bug in boto3 (https://github.com/boto/boto3/issues/1644)
# Details in https://github.com/jschneier/django-storages/issues/649
AWS_S3_ADDRESSING_STYLE = "path"

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=1209600",  # 2 weeks in seconds
}


# Static files (CSS, JavaScript, images)
STATIC_ROOT = "/files/assets"

STATIC_URL = env.str("DJANGO_STATIC_URL", default="/static/")
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, "static"),
    os.path.join(SITE_ROOT, "webapp", "build"),
)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="dummy key")

AUTH_USER_MODEL = "accounts.User"


# Static site url, used when we need absolute url but lack request object, e.g. in email sending.
SITE_URL = env.str("DJANGO_SITE_URL", default="http://127.0.0.1:8000")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])


# Don't allow site's content to be included in frames/iframes.
X_FRAME_OPTIONS = "DENY"


ROOT_URLCONF = f"{PROJECT_NAME}.urls"

WSGI_APPLICATION = f"{PROJECT_NAME}.wsgi.application"


LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "login"
LOGOUT_REDIRECT_URL = "login"


# Crispy-forms
CRISPY_TEMPLATE_PACK = "bootstrap4"


# Email config
DEFAULT_FROM_EMAIL = f"{PROJECT_TITLE} <info@rhizophora.xyz>"
SERVER_EMAIL = f"{PROJECT_TITLE} server <server@rhizophora.xyz>"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "mailhog"
EMAIL_PORT = 1025
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""


# Base logging config. Logs INFO and higher-level messages to console. Production-specific additions are in
#  production.py.
#  Notably we modify existing Django loggers to propagate and delegate their logging to the root handler, so that we
#  only have to configure the root handler.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d %(funcName)s - %(message)s"
        },
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "default"}},
    "loggers": {
        "": {"handlers": ["console"], "level": "INFO"},
        "django": {"handlers": [], "propagate": True},
        "django.request": {"handlers": [], "propagate": True},
        "django.security": {"handlers": [], "propagate": True},
    },
}

TEST_RUNNER = "django.test.runner.DiscoverRunner"


# Disable a few system checks. Careful with these, only silence what your really really don't need.
# TODO: check if this is right for your project.
SILENCED_SYSTEM_CHECKS = [
    "security.W001",  # we don't use SecurityMiddleware since security is better applied in nginx config
]

# Default values for sentry
# Example: https://TODO@sentry.thorgate.eu/TODO
SENTRY_DSN = env.str("DJANGO_SENTRY_DSN", default="")
SENTRY_ENVIRONMENT = env.str("DJANGO_SENTRY_ENVIRONMENT", default="local")

if SENTRY_DSN and not IS_DOCKER_BUILD:
    import sentry_sdk  # NOQA
    from sentry_sdk.integrations.django import DjangoIntegration  # NOQA

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        environment=SENTRY_ENVIRONMENT,
        # Send authenticated user information with sentry events (needs django.contrib.auth)
        send_default_pii=True,
    )

WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "",
        "STATS_FILE": os.path.join(SITE_ROOT, "webapp", "webpack-stats.json"),
    },
}

# All these settings will be made available to javascript app
SETTINGS_EXPORT = [
    "DEBUG",
    "SITE_URL",
    "STATIC_URL",
    "SENTRY_DSN",
    "SENTRY_ENVIRONMENT",
    "PROJECT_TITLE",
]

# django-js-reverse
JS_REVERSE_JS_VAR_NAME = "reverse"
JS_REVERSE_JS_GLOBAL_OBJECT_NAME = "DJ_CONST"
JS_REVERSE_EXCLUDE_NAMESPACES = ["admin", "djdt"]
