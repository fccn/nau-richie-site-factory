"""
End-to-end tests for the cookie bar
"""
from django.test.utils import override_settings

from cms.test_utils.testcases import CMSTestCase
from richie.apps.courses.factories import CourseFactory


class CookieBarBaseTemplateRenderingCMSTestCase(CMSTestCase):
    """
    Test case that verifies if the Cookie bar code is present.
    """

    @override_settings(COOKIE_BAR=True)
    def test_template_base_cookie_bar_present(self):
        """
        Tests if the Cookie bar code is added if the COOKIE_BAR setting is true.
        """
        course = CourseFactory()
        page = course.extended_object
        page.publish("en")

        url = course.extended_object.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "cookieconsent",
        )

    def test_template_base_cookie_bar_absent(self):
        """
        Tests if the Cookie bar code is not added if the COOKIE_BAR setting is not
        present.
        """
        course = CourseFactory()
        page = course.extended_object
        page.publish("en")

        url = course.extended_object.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(
            response,
            "cookieconsent",
        )
