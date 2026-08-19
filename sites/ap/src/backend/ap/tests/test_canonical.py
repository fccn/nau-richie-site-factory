"""
Test suite for the self-referencing canonical URL tag.
"""

from django.conf import settings
from django.test import TestCase, override_settings

from cms.api import create_page
from richie.apps.courses.factories import CourseFactory


class CanonicalUrlTestCase(TestCase):
    """Ensure indexable pages expose a correct, self-referencing canonical tag."""

    def test_homepage_has_self_referencing_canonical(self):
        """The homepage should carry a canonical tag pointing to itself."""
        page = create_page(
            "Home",
            "richie/homepage.html",
            settings.LANGUAGE_CODE,
            published=True,
        )
        page.set_as_homepage()

        response = self.client.get(page.get_absolute_url())

        self.assertContains(
            response,
            f'<link rel="canonical" href="http://example.com{page.get_absolute_url()}" />',
        )

    def test_course_detail_page_canonical_matches_its_own_clean_url(self):
        """
        A course detail page's canonical must point to its own clean URL - not the
        organization/category listing it's linked from, and not a redirected variant.
        """
        course = CourseFactory()
        course.extended_object.publish(settings.LANGUAGE_CODE)
        page = course.extended_object

        response = self.client.get(page.get_absolute_url())

        self.assertContains(
            response,
            f'<link rel="canonical" href="http://example.com{page.get_absolute_url()}" />',
        )

    def test_canonical_strips_pagination_query_string(self):
        """
        Visiting a detail page with a pagination query string (e.g. paginating an
        embedded course listing) must still canonicalize to the clean, unparameterized
        URL - consolidating ranking signals onto a single indexable version.
        """
        course = CourseFactory()
        course.extended_object.publish(settings.LANGUAGE_CODE)
        page = course.extended_object
        clean_url = page.get_absolute_url()

        response = self.client.get(f"{clean_url}?page_courses=2")

        self.assertContains(
            response,
            f'<link rel="canonical" href="http://example.com{clean_url}" />',
        )
        self.assertNotContains(response, "page_courses=2")

    def test_canonical_uses_https_behind_proxy(self):
        """
        The reverse proxy in front of this app terminates TLS and forwards plain
        HTTP. With SECURE_PROXY_SSL_HEADER configured (Production settings), the
        canonical URL must use https:// (the scheme the crawler actually requested),
        not the internal http:// one.
        """
        course = CourseFactory()
        course.extended_object.publish(settings.LANGUAGE_CODE)
        page = course.extended_object

        with override_settings(
            SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO", "https")
        ):
            response = self.client.get(
                page.get_absolute_url(), HTTP_X_FORWARDED_PROTO="https"
            )

        self.assertContains(response, 'rel="canonical" href="https://')
