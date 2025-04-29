import json

from django.conf import settings

import requests
from social_core.backends.oauth import BaseOAuth2


class EdxOAuth2Backend(BaseOAuth2):
    """Edx OAuth authentication backend"""

    name = "edx"
    AUTHORIZATION_URL = getattr(settings, "SOCIAL_AUTH_EDX_AUTHORIZATION_URL", "")
    ACCESS_TOKEN_URL = getattr(settings, "SOCIAL_AUTH_EDX_ACCESS_TOKEN_URL", "")
    ACCESS_TOKEN_METHOD = "POST"

    def get_user_details(self, response):
        """Return user details from Edx account"""
        return {
            "username": response.get("login"),
            "email": response.get("email") or "",
            "first_name": response.get("name"),
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = getattr(settings, "SOCIAL_AUTH_EDX_USER_DATA_URL", "")
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        data = requests.get(url, headers=headers)
        info = json.loads(data.content)

        return info if isinstance(info, dict) else {}
