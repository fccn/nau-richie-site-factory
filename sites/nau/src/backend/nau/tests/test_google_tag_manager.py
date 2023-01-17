"""
End-to-end tests for the course detail view
"""
from django.test.utils import override_settings

from cms.test_utils.testcases import CMSTestCase
from richie.apps.courses.factories import CourseFactory


class GoogleTagManagerBaseTemplateRenderingCMSTestCase(CMSTestCase):
    """
    Test case that verifies if the Google Tag Manager is being rendered and not using the Richie
    upstream Web Analytics.
    """

    @override_settings(GOOGLE_TAG_MANAGER_ID="xpto-key")
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
        GOOGLE_TAG_MANAGER_ENVIRONMENT="&gtm_auth=cexSLlJmC6wAalbsw6AuQA&gtm_preview=env-77&gtm_cookies_win=x",
    )
    def test_template_base_google_tag_manager_present_with_environment_config(self):
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
        print(response.content)
        self.assertContains(
            response,
            '"https://www.googletagmanager.com/ns.html?id=GTM-SOME-KEY&gtm_auth=cexSLlJmC6wAalbsw6AuQA&gtm_preview=env-77&gtm_cookies_win=x"',
        )
        self.assertContains(
            response,
            "GTM-SOME-KEY",
        )
        self.assertContains(
            response,
            "https://www.googletagmanager.com/gtm.js?id='+i+dl+'&gtm_auth=cexSLlJmC6wAalbsw6AuQA&gtm_preview=env-77&gtm_cookies_win=x';",
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
