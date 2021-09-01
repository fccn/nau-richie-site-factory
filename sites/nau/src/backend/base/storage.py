"""Customizing Django storage backends."""
from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """A S3Boto3Storage backend to serve media files via a CDN."""

    bucket_name = getattr(settings, "AWS_MEDIA_BUCKET_NAME", None)
    custom_domain = getattr(settings, "CDN_DOMAIN", None)
    file_overwrite = False
