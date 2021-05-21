from settings.local import *


SEND_EMAILS = False

DATABASES["default"]["TEST"] = {
    "NAME": "derf_test",
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
