"""
Tests for error views
"""

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.utils.translation import gettext_lazy as _

from cms.api import create_page
from richie.apps.core.views import error


class ErrorViewHandlersTestCase(TestCase):
    """Test suite for the custom NAU error view handlers"""

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
    def test_404_error_view_handler(self):
        """
        When a request does not found resource,
        the 404 error view should be displayed,
        and included with the arquivo404 js code.
        """
        page = create_page("Test", "richie/single_column.html", "en", published=True)
        request = RequestFactory().get("/")
        request.current_page = page
        request.user = AnonymousUser()
        with self.assertTemplateUsed("richie/error.html"):
            response = error.error_404_view_handler(request, Exception)
            self.assertContains(response, "arquivo.pt/arquivo404.js", status_code=404)
