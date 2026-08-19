"""
Shared test helpers for the nau backend test suite.
"""

from django.conf import settings
from django.test import override_settings

from richie.apps.courses.factories import CourseFactory


def create_published_course_page(**kwargs):
    """
    Create and publish a CourseFactory page in the default language, returning
    the underlying CMS page. Shared by tests that only need "some real,
    published page" to exercise page-level template tags (canonical, hreflang).
    """
    course = CourseFactory(**kwargs)
    course.extended_object.publish(settings.LANGUAGE_CODE)
    return course.extended_object


def get_with_https_proxy_header(client, url):
    """
    Perform a GET request simulating the reverse proxy's X-Forwarded-Proto
    header, with SECURE_PROXY_SSL_HEADER configured as it is under the
    Production settings class, so request.is_secure()/request.scheme
    correctly evaluate to https as they would in a real environment.
    """
    with override_settings(SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO", "https")):
        return client.get(url, HTTP_X_FORWARDED_PROTO="https")
