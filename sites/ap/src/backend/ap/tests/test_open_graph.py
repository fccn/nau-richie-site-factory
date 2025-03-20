"""
End-to-end tests for the language cookies
"""

from django.test import override_settings
from django.utils.translation import gettext_lazy as _

import lxml.html  # nosec
from cms.test_utils.testcases import CMSTestCase
from richie.apps.core.helpers import create_i18n_page


# pylint: disable=duplicate-code
class OpenGraphCMSTestCase(CMSTestCase):
    """
    Test case that verifies if the custom Open Graph image is used.
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
    def test_open_graph_image_homepage(self):
        """
        Test if the custom open graph image is used for the homepage.
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
        self.assertEqual(response.status_code, 200)
        html = lxml.html.fromstring(response.content)
        self.assertEqual(
            html.xpath("/html/head/meta[@property='og:image']")[0].get("content"),
            "http://testserver/static/richie/images/og_media_geral_fb_22a.png",
        )
