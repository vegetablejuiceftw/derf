from derf.celery import app as celery_app


default_app_config = "derf.apps.DerfConfig"

__all__ = ["celery_app"]
