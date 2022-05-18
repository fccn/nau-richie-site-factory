"""
End-to-end tests for the course detail view
"""
from django.test.utils import override_settings

from cms.test_utils.testcases import CMSTestCase
from richie.apps.courses.factories import CourseFactory


class ChatbotWidgetBaseTemplateRenderingCMSTestCase(CMSTestCase):
    """
    Test case that verifies if the Chatbot Widget is present.
    """

    @override_settings(CHATBOT_WIDGET_JS_URL="https://chatbot.nau.edu.pt/widget.js")
    def test_template_base_jira_widget_present(self):
        """
        Tests if the Chatbot widget code is added if the CHATBOT_WIDGET_JS_URL setting is
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
            "https://chatbot.nau.edu.pt/widget.js",
        )

    def test_template_base_jira_widget_absent(self):
        """
        Tests if the Chatbot widget code is not added if the CHATBOT_WIDGET_JS_URL setting is
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
            "https://chatbot.nau.edu.pt/widget.js",
        )
