"""
End-to-end tests for the language cookies
"""

from django.test.utils import override_settings

from cms.test_utils.testcases import CMSTestCase
from richie.apps.core.helpers import create_i18n_page


class LanguageCookiesCMSTestCase(CMSTestCase):
    """
    Test case that verifies if the language cookies settings are working.
    """

    @override_settings(
        LANGUAGE_COOKIE_NAME="cookie_name_for_language",
        LANGUAGE_COOKIE_DOMAIN="example.com",
    )
    def test_language_cookie_name(self):
        """
        Test if we change the `LANGUAGE_COOKIE_NAME` setting, it will change the response page
        language.
        """
        homepage = create_i18n_page(
            {
                "en": "Richie marketing homepage",
                "pt": "Página de entrada do marketing site Richie",
            },
            is_homepage=True,
        )
        homepage.publish("en")
        homepage.publish("pt")

        response = self.client.get("", follow=True)
        self.assertContains(
            response,
            "Richie marketing homepage",
        )
        self.assertEqual(
            "en", self.client.cookies.get("cookie_name_for_language").value
        )

        self.client.cookies.load({"cookie_name_for_language": "pt"})
        response = self.client.get("", follow=True)
        self.assertContains(
            response,
            "Página de entrada do marketing site Richie",
        )
        self.assertEqual(
            "pt", self.client.cookies.get("cookie_name_for_language").value
        )

        self.assertEqual(
            "example.com", self.client.cookies.get("cookie_name_for_language")["domain"]
        )
