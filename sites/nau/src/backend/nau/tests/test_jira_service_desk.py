"""
End-to-end tests for the course detail view
"""
from django.test.utils import override_settings

from cms.test_utils.testcases import CMSTestCase
from richie.apps.courses.factories import CourseFactory


class JiraServiceDeskWidgetBaseTemplateRenderingCMSTestCase(CMSTestCase):
    """
    Test case that verifies if the Jira Service Desk widget is present.
    """

    @override_settings(JIRA_WIDGET_KEY="xpto-key")
    def test_template_base_jira_widget_present(self):
        """
        Tests if the Jira Service Desk widget code is added if the JIRA_WIDGET_KEY setting is
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
            "jsd-widget.atlassian.com",
        )

    def test_template_base_jira_widget_absent(self):
        """
        Tests if the Jira Service Desk widget code is not added if the JIRA_WIDGET_KEY setting is
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
            "jsd-widget.atlassian.com",
        )
