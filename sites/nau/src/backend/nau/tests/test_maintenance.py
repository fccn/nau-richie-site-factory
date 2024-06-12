"""
End-to-end tests for the course detail view
"""

from django.test.utils import override_settings

from cms.test_utils.testcases import CMSTestCase
from richie.apps.courses.factories import CourseFactory


class MaintenanceBaseTemplateRenderingCMSTestCase(CMSTestCase):
    """
    Test case that verifies if the maintenance message is being displayed and the search on header
    if not visible.
    """

    @override_settings(MAINTENANCE_HEADER_MSG=True)
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

    @override_settings(MAINTENANCE_HEADER_MSG=False)
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
