"""Open edX OAuth authentication backend"""

import json

from django.conf import settings

import requests
from social_core.backends.oauth import BaseOAuth2


# pylint: disable=abstract-method
class OpenEdxOAuth2Backend(BaseOAuth2):
    """Open edX `BaseOAuth2` backend implementation"""

    name = "open_edx"
    AUTHORIZATION_URL = getattr(settings, "SOCIAL_AUTH_OPEN_EDX_AUTHORIZATION_URL", "")
    ACCESS_TOKEN_URL = getattr(settings, "SOCIAL_AUTH_OPEN_EDX_ACCESS_TOKEN_URL", "")
    ACCESS_TOKEN_METHOD = "POST"  # nosec

    def get_user_details(self, response):
        """Return user details from Open edX account"""
        return {
            "username": response.get("login"),
            "email": response.get("email") or "",
            "first_name": response.get("name"),
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = getattr(settings, "SOCIAL_AUTH_OPEN_EDX_USER_DATA_URL", "")
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        data = requests.get(url, headers=headers, timeout=20)
        info = json.loads(data.content)

        return info if isinstance(info, dict) else {}
