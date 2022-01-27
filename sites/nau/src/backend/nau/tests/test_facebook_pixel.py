"""
End-to-end tests for the course detail view
"""
from django.test.utils import override_settings

from cms.test_utils.testcases import CMSTestCase
from richie.apps.courses.factories import CourseFactory


class FacebookPixelBaseTemplateRenderingCMSTestCase(CMSTestCase):
    """
    Test case that verifies if the Facebook Pixel code is present.
    """

    @override_settings(FACEBOOK_PIXEL_ID="xpto-key")
    def test_template_base_facebook_pixel_present(self):
        """
        Tests if the Facebook Pixel code is added if the FACEBOOK_PIXEL_ID setting is present.
        """
        course = CourseFactory()
        page = course.extended_object
        page.publish("en")

        url = course.extended_object.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "connect.facebook.net/en_US/fbevents.js",
        )
        self.assertContains(
            response,
            "xpto-key",
        )

    def test_template_base_facebook_pixel_absent(self):
        """
        Tests if the Facebook Pixel code is not added if the FACEBOOK_PIXEL_ID setting is not
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
            "connect.facebook.net/en_US/fbevents.js",
        )
