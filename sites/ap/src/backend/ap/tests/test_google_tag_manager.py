"""
End-to-end tests for the course detail view
"""

from django.test.utils import override_settings
from django.utils.translation import gettext_lazy as _

from cms.test_utils.testcases import CMSTestCase
from richie.apps.courses.factories import CourseFactory


# pylint: disable=duplicate-code
class GoogleTagManagerBaseTemplateRenderingCMSTestCase(CMSTestCase):
    """
    Test case that verifies if the Google Tag Manager is being rendered and not using the Richie
    upstream Web Analytics.
    """

    @override_settings(
        WEB_ANALYTICS={"google_tag_manager": {"tracking_id": "xpto-key"}},
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
    def test_template_base_google_tag_manager_present(self):
        """
        Tests if the Google Tag Manager code is added if the GOOGLE_TAG_MANAGER_ID setting is
        present.
        """
        course = CourseFactory()
        page = course.extended_object
        page.publish("en")

        url = course.extended_object.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "www.googletagmanager.com/gtm.js?id='+i+dl+'';",
        )
        self.assertContains(
            response,
            "dataLayer','xpto-key'",
        )
        self.assertContains(
            response,
            '"https://www.googletagmanager.com/ns.html?id=xpto-key"',
        )
        self.assertContains(
            response,
            "xpto-key",
        )

    @override_settings(
        GOOGLE_TAG_MANAGER_ID="GTM-SOME-KEY",
        WEB_ANALYTICS={
            "google_tag_manager": {
                "tracking_id": "GTM-SOME-KEY",
                "environment": "&gtm_auth=cexSLlJmC6wAalbsw6AuQA&gtm_preview=env-77&gtm_cookies_win=x",  # noqa pylint: disable=line-too-long
            }
        },
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
    def test_template_base_google_tag_manager_present_with_environment_config(self):
        """
        Tests if the Google Tag Manager code is added if the environment configuration is
        present.
        """

        course = CourseFactory()
        page = course.extended_object
        page.publish("en")

        url = course.extended_object.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "www.googletagmanager.com/gtm.js",
        )
        self.assertContains(
            response,
            "dataLayer','GTM-SOME-KEY'",
        )
        self.assertContains(
            response,
            '"https://www.googletagmanager.com/ns.html?id=GTM-SOME-KEY&gtm_auth=cexSLlJmC6wAalbsw6AuQA&gtm_preview=env-77&gtm_cookies_win=x"',  # noqa pylint: disable=line-too-long
        )
        self.assertContains(
            response,
            "GTM-SOME-KEY",
        )
        self.assertContains(
            response,
            "https://www.googletagmanager.com/gtm.js?id='+i+dl+'&gtm_auth=cexSLlJmC6wAalbsw6AuQA&gtm_preview=env-77&gtm_cookies_win=x';",  # noqa pylint: disable=line-too-long
        )

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
    def test_template_base_google_tag_manager_absent(self):
        """
        Tests if the Google Tag Manager code is not added if the GOOGLE_TAG_MANAGER_ID setting is
        not present.
        """
        course = CourseFactory()
        page = course.extended_object
        page.publish("en")

        url = course.extended_object.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(
            response,
            "www.googletagmanager.com/gtm.js",
        )
        self.assertNotContains(
            response,
            '"https://www.googletagmanager.com/ns.html"',
        )
