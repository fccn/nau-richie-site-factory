"""
Test suite for the hreflang <link rel="alternate"> tags (richie's own template).
"""

from django.conf import settings
from django.test import TestCase

from richie.apps.courses.factories import CourseFactory

from . import create_published_course_page, get_with_https_proxy_header


class HreflangTestCase(TestCase):
    """
    Ensure hreflang alternate-language URLs are absolute, HTTPS, and never point
    to a redirected/stale page - see fccn/nau-technical#993.
    """

    def test_course_detail_page_has_hreflang_for_default_language(self):
        """A published course page must expose a self-referencing hreflang entry."""
        page = create_published_course_page()

        response = self.client.get(page.get_absolute_url())

        self.assertContains(
            response,
            f'<link rel="alternate" href="http://example.com{page.get_absolute_url()}"'
            f' hreflang="{settings.LANGUAGE_CODE}" />',
        )

    def test_hreflang_target_resolves_without_redirect(self):
        """
        Every hreflang target must be a direct, final URL - not one that 301s
        elsewhere (e.g. a stale slug or a language-prefix redirect). This is the
        crawler-facing property that #993 is actually about.
        """
        page = create_published_course_page()

        response = self.client.get(page.get_absolute_url())
        content = response.content.decode()

        start = content.index('<link rel="alternate" href="')
        start += len('<link rel="alternate" href="')
        end = content.index('"', start)
        hreflang_url = content[start:end]
        # Strip the scheme+host prefix injected by SITE.web_url to hit the path locally.
        path = hreflang_url.split("example.com", 1)[1]

        follow_up = self.client.get(path)

        self.assertEqual(follow_up.status_code, 200)

    def test_hreflang_uses_https_behind_proxy(self):
        """
        The reverse proxy in front of this app terminates TLS and forwards plain
        HTTP. With SECURE_PROXY_SSL_HEADER configured (Production settings), the
        hreflang href must use https:// (the scheme the crawler actually requested),
        not the internal http:// one - otherwise crawlers see an hreflang URL that
        immediately 301-redirects to https, which is exactly the #993 bug.
        """
        page = create_published_course_page()

        response = get_with_https_proxy_header(self.client, page.get_absolute_url())

        self.assertContains(response, 'rel="alternate" href="https://')

    def test_untranslated_page_hreflang_falls_back_to_other_language(self):
        """
        A page that only exists in one language still emits an hreflang entry
        for every configured language (richie's hreflang.html loops over all of
        them unconditionally) - see fccn/nau-technical#994. For the language
        that has no translation, page_language_url falls back to the other
        language's URL (per CMS_LANGUAGES fallbacks), so the hreflang target is
        never omitted and never a broken link/404 - it resolves 200 and serves
        the fallback-language content under the other language's URL prefix.
        This test documents that behaviour as the chosen strategy for #994's
        "untranslated pages" requirement, rather than a bug.
        """
        course = CourseFactory()
        course.extended_object.publish("en")
        page = course.extended_object

        self.assertEqual(page.get_published_languages(), ["en"])

        response = self.client.get(page.get_absolute_url("en"))
        content = response.content.decode()

        # Both an "en" self-reference and a "pt-PT" entry are present...
        self.assertIn('hreflang="en"', content)
        self.assertIn('hreflang="pt-PT"', content)

        # ...and the "pt-PT" entry's target resolves (200, no redirect/404)
        # even though the page has no Portuguese translation.
        start = content.index('hreflang="pt-PT"')
        href_start = content.rindex('href="', 0, start) + len('href="')
        href_end = content.index('"', href_start)
        pt_href = content[href_start:href_end]
        pt_path = pt_href.split("example.com", 1)[1]

        pt_response = self.client.get(pt_path)

        self.assertEqual(pt_response.status_code, 200)

    def test_hreflang_uses_region_qualified_portuguese_code(self):
        """
        Per fccn/nau-technical#994, the Portuguese hreflang value must be the
        region-qualified "pt-PT" (not the bare "pt" that the URL/CMS language
        code itself uses), while "en" is intentionally left unqualified. Only
        the hreflang attribute changes - the URL path stays "/pt/..." as before.
        """
        course = CourseFactory(page_languages=["en", "pt"], should_publish=True)
        page = course.extended_object

        response = self.client.get(page.get_absolute_url("en"))
        content = response.content.decode()

        self.assertIn('hreflang="en"', content)
        self.assertIn('hreflang="pt-PT"', content)
        self.assertNotIn('hreflang="pt"', content)
        # The href target itself must still use the plain "/pt/" URL prefix.
        self.assertIn(
            f'href="http://example.com{page.get_absolute_url("pt")}"', content
        )
