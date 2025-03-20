"""
End-to-end tests for the course detail view
"""

from django.test.utils import override_settings
from django.utils.translation import gettext_lazy as _

from cms.test_utils.testcases import CMSTestCase
from richie.apps.courses.factories import CourseFactory


# pylint: disable=duplicate-code
class MaintenanceBaseTemplateRenderingCMSTestCase(CMSTestCase):
    """
    Test case that verifies if the maintenance message is being displayed and the search on header
    if not visible.
    """

    @override_settings(
        MAINTENANCE_HEADER_MSG=True,
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
    def test_template_base_maintenance_is_true(self):
        """
        Test if the maintenance message is visible on header if MAINTENANCE_HEADER_MSG is true.
        """
        course = CourseFactory()
        page = course.extended_object
        page.publish("en")

        url = course.extended_object.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "topbar__maintenance")
        self.assertNotContains(response, "topbar__search")

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
    def test_template_base_maintenance_is_absent(self):
        """
        Test if the maintenance message is not visible if the `MAINTENANCE_HEADER_MSG` not defined
        and the top bar search is visible.
        """
        course = CourseFactory()
        page = course.extended_object
        page.publish("en")

        url = course.extended_object.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, "topbar__maintenance")
        self.assertContains(response, "topbar__search")

    @override_settings(
        MAINTENANCE_HEADER_MSG=False,
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
    def test_template_base_maintenance_is_false(self):
        """
        Test if the maintenance message is not visible if the `MAINTENANCE_HEADER_MSG` is False
        and the top bar search is visible.
        """
        course = CourseFactory()
        page = course.extended_object
        page.publish("en")

        url = course.extended_object.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, "topbar__maintenance")
        self.assertContains(response, "topbar__search")
