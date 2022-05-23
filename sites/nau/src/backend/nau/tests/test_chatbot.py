"""
End-to-end tests for the course detail view
"""
from django.test.utils import override_settings

from cms.test_utils.testcases import CMSTestCase
from richie.apps.courses.factories import CourseFactory, OrganizationFactory


class ChatbotWidgetBaseTemplateRenderingCMSTestCase(CMSTestCase):
    """
    Test case that verifies if the Chatbot Widget is present.
    """

    @override_settings(CHATBOT_WIDGET_JS_URL="https://chatbot.nau.edu.pt/widget.js")
    def test_templates_nau_chatbot_present(self):
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

    def test_templates_nau_chatbot_absent(self):
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

    @override_settings(CHATBOT_WIDGET_JS_URL="https://chatbot.nau.edu.pt/widget.js")
    def test_templates_nau_chatbot_course_param(self):
        """
        Tests if the Chatbot widget contains the course parameter.
        """
        org_page_code = "MY_ORG"
        organization = OrganizationFactory(
            should_publish=True, code=org_page_code, page_title="One of the partners"
        )

        course_page_code = "MY_COURSE"
        course_page_title = {
            "en": "A good course to learn something",
        }
        course = CourseFactory(
            page_title=course_page_title,
            fill_organizations=[organization],
            code=course_page_code,
        )

        page = course.extended_object
        page.publish("en")
        url = page.get_absolute_url(language="en")
        response = self.client.get(url)

        self.assertContains(
            response,
            's.setAttribute("param_curso", "A good course to learn something-MY_ORG-MY_COURSE");',
        )
