"""
Tests for the course runs synchronization from the LMS.
"""

import copy
from unittest import mock

from django.conf import settings
from django.test import TestCase, override_settings

from richie.apps.courses.api import sync_course_run
from richie.apps.courses.factories import CourseFactory, CourseRunFactory
from richie.apps.courses.models import CourseRun, CourseRunSyncMode

LMS_BASE_URL = "https://lms.example.org"
COURSE_REGEX = r"^.*/courses/(?P<course_id>.*)/course/?$"
CANONICAL_LINK = f"{LMS_BASE_URL}/courses/course-v1:org+CODE+2025_T1/course/"
LOWERCASE_LINK = f"{LMS_BASE_URL}/courses/course-v1:org+code+2025_T1/course/"


class CourseRunSyncTestCase(TestCase):
    """The sync must never rewrite the resource link of an existing course run."""

    def test_resource_link_is_protected_from_sync_updates(self):
        """
        Guard the setting itself, so that it cannot silently be dropped by a future
        refactoring of the LMS configuration.
        """
        no_update_fields = settings.RICHIE_LMS_BACKENDS[0][
            "COURSE_RUN_SYNC_NO_UPDATE_FIELDS"
        ]

        self.assertIn("resource_link", no_update_fields)

    def test_sync_with_differently_cased_link_keeps_resource_link(self):
        """
        The LMS builds the resource link from the course key as it received it, whose
        casing can differ from the canonical one. MySQL matches the link
        case-insensitively, so the sync finds the existing course run: its link must
        not be overwritten, while the other fields are still synchronized.
        """
        lms_backends = copy.deepcopy(settings.RICHIE_LMS_BACKENDS)
        lms_backends[0]["BASE_URL"] = LMS_BASE_URL
        lms_backends[0]["COURSE_REGEX"] = COURSE_REGEX

        course = CourseFactory(code="CODE")
        course_run = CourseRunFactory(
            direct_course=course,
            resource_link=CANONICAL_LINK,
            sync_mode=CourseRunSyncMode.SYNC_TO_PUBLIC,
            enrollment_count=1,
        )

        original_filter = CourseRun.objects.filter

        def case_insensitive_filter(*args, **kwargs):
            """Emulate the case-insensitive matching of MySQL on any database."""
            if "resource_link" in kwargs:
                kwargs["resource_link__iexact"] = kwargs.pop("resource_link")
            return original_filter(*args, **kwargs)

        with override_settings(RICHIE_LMS_BACKENDS=lms_backends), mock.patch.object(
            CourseRun.objects, "filter", case_insensitive_filter
        ):
            sync_course_run(
                {
                    "resource_link": LOWERCASE_LINK,
                    "start": "2030-01-01T00:00:00Z",
                    "end": "2030-06-01T00:00:00Z",
                    "enrollment_start": "2029-12-01T00:00:00Z",
                    "enrollment_end": "2030-05-01T00:00:00Z",
                    "languages": ["pt"],
                    "enrollment_count": 42,
                }
            )

        course_run.refresh_from_db()
        self.assertEqual(course_run.resource_link, CANONICAL_LINK)
        self.assertEqual(course_run.enrollment_count, 42)
