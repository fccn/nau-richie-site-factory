"""
End-to-end tests for the course detail view
"""

from cms.test_utils.testcases import CMSTestCase
from richie.apps.courses.factories import CourseFactory, OrganizationFactory


# pylint: disable=duplicate-code
class RedirectsCMSTestCase(CMSTestCase):
    """
    Test Redirects from Open edX to Richie.
    """

    def test_redirects_openedx_lms_course_page_about(self):
        """
        Test redirect to course page from a path of Open edX LMS course about page.
        """
        course = CourseFactory(code="DemoX")
        page = course.extended_object
        page.publish("en")

        response = self.client.get("/courses/course-v1:acme+DemoX+session01/about")

        url = course.extended_object.get_absolute_url(language="en")
        self.assertRedirects(response, url, status_code=301)

    def test_redirects_openedx_lms_course_page_course(self):
        """
        Test redirect to course page from a path of Open edX LMS course page.
        """
        course = CourseFactory(code="DemoX")
        page = course.extended_object
        page.publish("en")

        response = self.client.get("/courses/course-v1:acme+DemoX+session01/course/")

        url = course.extended_object.get_absolute_url(language="en")
        self.assertRedirects(response, url, status_code=301)

    def test_redirects_openedx_lms_course_course_modes_choose(self):
        """
        Test redirect to course page from a path of Open edX LMS course modes choose page.
        """
        course = CourseFactory(code="DemoX")
        page = course.extended_object
        page.publish("en")

        response = self.client.get(
            "/course_modes/choose/course-v1:acme+DemoX+session01/"
        )

        url = course.extended_object.get_absolute_url(language="en")
        self.assertRedirects(response, url, status_code=301)

    def test_redirects_openedx_cms_course_settings_detail(self):
        """
        Test redirect to course page from a path of Open edX Studio course settings details.
        """
        course = CourseFactory(code="DemoX")
        page = course.extended_object
        page.publish("en")

        response = self.client.get("/settings/details/course-v1:acme+DemoX+session01")

        url = course.extended_object.get_absolute_url(language="en")
        self.assertRedirects(response, url, status_code=301)

    def test_redirects_course_code(self):
        """
        Test redirect to course page from course code.
        """
        course = CourseFactory(code="DemoX")
        page = course.extended_object
        page.publish("en")

        response = self.client.get("/redirects/courses/DemoX/")

        url = course.extended_object.get_absolute_url(language="en")
        self.assertRedirects(response, url, status_code=301)

    def test_redirects_organization_code(self):
        """
        Test redirect to organization page from organization code.
        """
        organization = OrganizationFactory(code="acme")
        page = organization.extended_object
        page.publish("en")

        response = self.client.get("/redirects/partners/acme/")

        url = organization.extended_object.get_absolute_url(language="en")
        self.assertRedirects(response, url, status_code=301)
