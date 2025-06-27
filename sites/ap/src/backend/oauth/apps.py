"""`outh` app config definition"""

from django.apps import AppConfig


class OauthConfig(AppConfig):
    """`AppConfig` implementation for `oauth` app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "oauth"
