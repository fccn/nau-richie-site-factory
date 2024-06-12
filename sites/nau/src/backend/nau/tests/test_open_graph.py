"""
End-to-end tests for the language cookies
"""

import lxml.html  # nosec
from cms.test_utils.testcases import CMSTestCase
from richie.apps.core.helpers import create_i18n_page


class OpenGraphCMSTestCase(CMSTestCase):
    """
    Test case that verifies if the custom Open Graph image is used.
    """

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
