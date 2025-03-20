"""
End-to-end tests for the course detail view
"""

from django.test import override_settings
from django.utils.translation import gettext_lazy as _

from cms.test_utils.testcases import CMSTestCase
from richie.apps.core.helpers import create_i18n_page


class RedirectWidgetBaseTemplateRenderingCMSTestCase(CMSTestCase):
    """
    Test case that verifies if the redirect message is being displayed and the search on header
    if not visible.
    """

    @override_settings(
        RFC_5646_LOCALES=["en-US", "pt-PT"],
        LANGUAGE_CODE="en",
        LANGUAGES=(("en", _("English Lang")), ("pt", _("Portuguese Lang"))),
        CMS_LANGUAGES={
            "default": {
                "public": True,
                "hide_untranslated": False,
                "redirect_on_fallback": True,
                "fallbacks": ["en", "pt"],
            },
            1: [
                {
                    "public": True,
                    "code": "en",
                    "hide_untranslated": False,
                    "name": _("English Lang"),
                    "fallbacks": ["pt"],
                    "redirect_on_fallback": False,
                },
                {
                    "public": True,
                    "code": "pt",
                    "hide_untranslated": False,
                    "name": _("Portuguese Lang"),
                    "fallbacks": ["en"],
                    "redirect_on_fallback": False,
                },
            ],
        },
    )
    def test_redirect_course_page(self):
        """
        Test if we change the `LANGUAGE_COOKIE_NAME` setting, it will change the response page
        language.
        """
        args = {"redirect": "/en/courses/"}
        parent_course_page = create_i18n_page(
            {
                "en": "Parent course page without course search",
                "pt": "Página pai de todos os cursos sem pesquisa",
            },
            **args
        )
        parent_course_page.publish("en")
        parent_course_page.publish("pt")

        url = parent_course_page.get_absolute_url(language="en")
        response = self.client.get(url + "?organizations=1")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/en/courses/?organizations=1")
