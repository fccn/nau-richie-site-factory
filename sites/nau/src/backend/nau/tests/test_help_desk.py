"""
End-to-end tests for the course detail view
"""
from django.test.utils import override_settings

from cms.test_utils.testcases import CMSTestCase
from richie.apps.courses.factories import CourseFactory


class HelpDeskUrlBaseTemplateRenderingCMSTestCase(CMSTestCase):
    """
    Test case that verifies if the help url is available in the topbar.
    """

    @override_settings(HELP_DESK_URL="https://ajuda.nau.edu.pt")
    def test_template_base_help_url_present(self):
        """
        Tests if the help desk url for users is present in HELP_DESK_URL
        """
        course = CourseFactory()
        page = course.extended_object
        page.publish("en")

        url = course.extended_object.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "https://ajuda.nau.edu.pt",
        )

    def test_template_base_help_url_absent(self):
        """
        Tests if the help desk url for users is not present in HELP_DESK_URL
        """
        course = CourseFactory()
        page = course.extended_object
        page.publish("en")

        url = course.extended_object.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(
            response,
            "https://ajuda.nau.edu.pt",
        )
