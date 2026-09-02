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

    def test_robots_txt_does_not_disallow_parameterized_urls(self):
        """
        A prior version of this file added "Disallow: *?*" to keep crawlers away
        from query-string URLs (pagination, search filters, UTM params). This was
        reverted (fccn/nau-technical#991) because it conflicts with the
        self-referencing canonical tag strategy (fccn/nau-technical#993): Google
        explicitly recommends against using robots.txt for canonicalization,
        since a disallowed page can still get indexed (e.g. via an external link)
        without Google ever crawling it to read its canonical tag, which prevents
        link-signal consolidation onto the clean URL instead of just achieving it
        via crawling+following the canonical tag as intended. The canonical tag
        alone already fully handles duplicate-content consolidation for these
        URLs, so no robots.txt block is needed on top of it.
        """
        response = self.client.get("/robots.txt")

        self.assertNotContains(response, "Disallow")

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
