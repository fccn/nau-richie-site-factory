"""
Test suite for the cached sitemap.xml view.
"""

import re
from unittest import mock

from django.conf import settings
from django.core.cache import cache
from django.test import TestCase, override_settings

from cms.sitemaps import CMSSitemap
from richie.apps.courses.factories import CourseFactory


@override_settings(
    CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}},
    SITEMAP_CACHE_TIMEOUT=86400,
)
class SitemapCacheTestCase(TestCase):
    """Ensure sitemap.xml is served from cache instead of being rebuilt on every request."""

    def setUp(self):
        super().setUp()
        cache.clear()
        course = CourseFactory()
        course.extended_object.publish(settings.LANGUAGE_CODE)

    def test_sitemap_returns_200_xml(self):
        """The sitemap endpoint should respond successfully with an XML document."""
        response = self.client.get("/sitemap.xml")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")

    def test_sitemap_generation_is_not_repeated_on_second_request(self):
        """
        A second request within the cache timeout should be served entirely from
        cache: the (expensive) sitemap generation itself must only run once, no
        matter how many times crawlers hit the endpoint in that window.
        """
        with mock.patch.object(
            CMSSitemap, "items", wraps=CMSSitemap.items, autospec=True
        ) as mocked_items:
            first_response = self.client.get("/sitemap.xml")
            second_response = self.client.get("/sitemap.xml")

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(
            mocked_items.call_count,
            1,
            "Sitemap generation should only run once for both requests; the second "
            "request should be served from cache",
        )
        self.assertEqual(first_response.content, second_response.content)

    def test_sitemap_sets_cache_control_header(self):
        """The cached view should set a Cache-Control header advertising its lifetime."""
        response = self.client.get("/sitemap.xml")

        self.assertIn("Cache-Control", response)
        self.assertIn("max-age=", response["Cache-Control"])

    def test_sitemap_urls_use_https_behind_proxy(self):
        """
        The reverse proxy in front of this app terminates TLS and forwards plain
        HTTP, setting an X-Forwarded-Proto header. With SECURE_PROXY_SSL_HEADER
        configured (Production settings), <loc> entries must use https:// (the
        scheme the crawler actually requested), not the internal http:// one.
        """
        with override_settings(
            SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO", "https")
        ):
            response = self.client.get("/sitemap.xml", HTTP_X_FORWARDED_PROTO="https")

        self.assertContains(response, "<loc>https://")
        self.assertNotContains(response, "<loc>http://")

    def test_sitemap_never_relies_on_query_string_urls(self):
        """
        Query-string URLs (pagination, search filters, UTM params) are not unique
        indexable content - every indexable page already has a clean, path-based
        URL the sitemap can point crawlers to. Listing a query-string URL in the
        sitemap would advertise a non-canonical variant for indexing instead of
        the clean URL the self-referencing canonical tag (fccn/nau-technical#993)
        points to for that same content, working against the canonical strategy
        rather than reinforcing it.
        """
        response = self.client.get("/sitemap.xml")

        for loc in re.findall(rb"<loc>([^<]+)</loc>", response.content):
            self.assertNotIn(
                b"?",
                loc,
                f"Sitemap entry {loc} contains a query string, which is a "
                "non-canonical URL variant that should not be advertised for "
                "indexing",
            )
