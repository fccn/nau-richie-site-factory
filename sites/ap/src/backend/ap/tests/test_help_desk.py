"""
End-to-end tests for the course detail view
"""

from django.conf import settings
from django.test.utils import override_settings

from cms.test_utils.testcases import CMSTestCase
from richie.apps.courses.factories import CourseFactory


class HelpDeskUrlBaseTemplateRenderingCMSTestCase(CMSTestCase):
    """
    Test case that verifies if the help url is available in the topbar.
    """

    def setUp(self):
        self.language = getattr(settings, "LANGUAGE_CODE", "pt")

    @override_settings(HELP_DESK_URL="https://ajuda.ap.nau.edu.pt")
    def test_template_base_help_url_present(self):
        """
        Tests if the help desk url for users is present in HELP_DESK_URL
        """
        course = CourseFactory()
        page = course.extended_object
        page.publish(self.language)

        url = course.extended_object.get_absolute_url(language=self.language)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "https://ajuda.ap.nau.edu.pt",
        )

    def test_template_base_help_url_absent(self):
        """
        Tests if the help desk url for users is not present in HELP_DESK_URL
        """
        course = CourseFactory()
        page = course.extended_object
        page.publish(self.language)

        url = course.extended_object.get_absolute_url(language=self.language)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(
            response,
            "https://ajuda.ap.nau.edu.pt",
        )
