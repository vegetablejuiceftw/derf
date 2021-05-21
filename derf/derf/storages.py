from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage


class PrivateMediaStorage(S3Boto3Storage):
    """Media storage which disables public access by default

    When you use this as the default storage it makes sense to
    turn off all public access to the bucket.
    """

    location = settings.MEDIAFILES_LOCATION
    default_acl = "private"


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    default_acl = "public-read"
