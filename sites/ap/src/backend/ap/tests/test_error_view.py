"""
Tests for error views
"""

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.test.client import RequestFactory

from cms.api import create_page
from richie.apps.core.views import error


class ErrorViewHandlersTestCase(TestCase):
    """Test suite for the custom NAU error view handlers"""

    def setUp(self):
        self.language = getattr(settings, "LANGUAGE_CODE", "pt")

    def test_404_error_view_handler(self):
        """
        When a request does not found resource,
        the 404 error view should be displayed,
        and included with the arquivo404 js code.
        """
        page = create_page(
            "Test", "richie/single_column.html", self.language, published=True
        )
        request = RequestFactory().get("/")
        request.current_page = page
        request.user = AnonymousUser()
        with self.assertTemplateUsed("richie/error.html"):
            response = error.error_404_view_handler(request, Exception)
            self.assertContains(response, "arquivo.pt/arquivo404.js", status_code=404)
