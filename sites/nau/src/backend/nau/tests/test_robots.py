"""
Test suite for the robots.txt view.
"""

from django.test import TestCase, override_settings


class RobotsTxtTestCase(TestCase):
    """Ensure robots.txt is served correctly and advertises the right crawl rules."""

    def test_robots_txt_returns_200_plain_text(self):
        """The robots.txt endpoint should respond successfully as plain text."""
        response = self.client.get("/robots.txt")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")

    def test_robots_txt_disallows_parameterized_urls(self):
        """
        Query-string URLs (pagination on detail pages, client-side search filters,
        UTM tracking params...) are not unique indexable content on this site - all
        real content lives at clean, path-based URLs already listed in the sitemap.
        Crawling them wastes crawl budget and can surface near-duplicate content.
        """
        response = self.client.get("/robots.txt")

        self.assertContains(response, "Disallow: *?*")

    def test_robots_txt_sitemap_reference_uses_https_behind_proxy(self):
        """
        The reverse proxy in front of this app terminates TLS and forwards plain
        HTTP, setting an X-Forwarded-Proto header. With SECURE_PROXY_SSL_HEADER
        configured (Production settings), the Sitemap: line must reflect the
        original https:// scheme instead of the internal http:// one.
        """
        with override_settings(
            SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO", "https")
        ):
            response = self.client.get("/robots.txt", HTTP_X_FORWARDED_PROTO="https")

        self.assertContains(response, "Sitemap: https://")
