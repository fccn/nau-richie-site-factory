"""
End-to-end tests for the course detail view
"""

from django.conf import settings

from cms.test_utils.testcases import CMSTestCase
from richie.apps.core.helpers import create_i18n_page


class RedirectWidgetBaseTemplateRenderingCMSTestCase(CMSTestCase):
    """
    Test case that verifies if the redirect message is being displayed and the search on header
    if not visible.
    """

    def setUp(self):
        self.language = getattr(settings, "LANGUAGE_CODE", "pt")

    def test_redirect_course_page(self):
        """
        Test if we change the `LANGUAGE_COOKIE_NAME` setting, it will change the response page
        language.
        """
        args = {"redirect": f"/{self.language}/cursos/"}
        parent_course_page = create_i18n_page(
            {
                self.language: "Página pai de todos os cursos sem pesquisa",
            },
            **args,
        )
        parent_course_page.publish(self.language)

        url = parent_course_page.get_absolute_url(language=self.language)
        response = self.client.get(url + "?organizacoes=1")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/{self.language}/cursos/?organizacoes=1")
