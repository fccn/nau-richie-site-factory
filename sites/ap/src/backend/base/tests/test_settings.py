"""Test cnfpt configuration."""

from unittest import mock

from django.conf import settings
from django.test import TestCase, override_settings
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework.settings import DEFAULTS, api_settings
from richie.apps.search.viewsets.courses import CoursesViewSet


@override_settings(
    RFC_5646_LOCALES=["en-US", "pt-PT"],
    LANGUAGE_CODE="en",
    LANGUAGES=(("en", _("English Lang")), ("pt", _("Portuguese Lang"))),
    CMS_LANGUAGES={
        "default": {
            "public": True,
            "hide_untranslated": False,
            "redirect_on_fallback": True,
            "fallbacks": ["en", "pt"],
        },
        1: [
            {
                "public": True,
                "code": "en",
                "hide_untranslated": False,
                "name": _("English Lang"),
                "fallbacks": ["pt"],
                "redirect_on_fallback": False,
            },
            {
                "public": True,
                "code": "pt",
                "hide_untranslated": False,
                "name": _("Portuguese Lang"),
                "fallbacks": ["en"],
                "redirect_on_fallback": False,
            },
        ],
    },
)
class ConfigurationTestCase(TestCase):
    """Validate that our configuration works as expected."""

    @mock.patch.object(CoursesViewSet, "list", spec=True, return_value=Response({}))
    def test_configuration_restframework_htaccess(self, _mock_list):
        """The search API endpoint should work behind an htaccess."""
        # First, check that API calls were broken with the default DRF configuration
        # What was happening is that DRF defines Basic Authentication as a fallback by default
        # and our query has a basic auth header with the username and password of the htaccess
        # defined in nginx. Django was trying to authenticate a user with these credentials,
        # which of course failed.
        with override_settings(
            REST_FRAMEWORK={
                **settings.REST_FRAMEWORK,
                "DEFAULT_AUTHENTICATION_CLASSES": DEFAULTS[
                    "DEFAULT_AUTHENTICATION_CLASSES"
                ],
            }
        ):
            authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES

        # The authentication classes are loaded before settings are overriden so we need
        # to mock them on the APIView
        with mock.patch(
            "rest_framework.views.APIView.authentication_classes",
            new_callable=mock.PropertyMock,
            return_value=authentication_classes,
        ):
            response = self.client.get(
                "/api/v1.0/courses/",
                HTTP_AUTHORIZATION="Basic dXNlcm5hbWU6cGFzc3dvcmQ=",
            )
        self.assertEqual(response.status_code, 403)

        # Check that the project configuration solves it
        response = self.client.get(
            "/api/v1.0/courses/", HTTP_AUTHORIZATION="Basic dXNlcm5hbWU6cGFzc3dvcmQ="
        )
        self.assertEqual(response.status_code, 200)
