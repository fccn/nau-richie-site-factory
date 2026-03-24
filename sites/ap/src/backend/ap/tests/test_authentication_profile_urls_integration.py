"""Integration tests for authentication profile URLs."""

from django.conf import settings
from django.test import TestCase, override_settings


class AuthenticationProfileURLsIntegrationTestCase(TestCase):
    """Integration tests for profile URLs with base_url and username substitution."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_url = "https://lms.example.com"
        self.test_username = "johndoe"

    def test_url_base_url_substitution_pattern(self):
        """Test that URLs are structured for base_url substitution."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]

        # Simulate what the frontend would do to substitute base_url
        for _key, url_config in profile_urls.items():
            href = url_config["href"]
            # The frontend should replace {base_url:s} with the actual base URL
            if "{base_url:s}" in href:
                substituted_url = href.format(base_url=self.base_url)
                self.assertNotIn("{base_url:s}", substituted_url)
                self.assertIn(self.base_url, substituted_url)

    def test_dashboard_url_construction(self):
        """Test dashboard URL construction with base_url."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]
        dashboard_href = profile_urls["dashboard"]["href"]

        # Construct the full URL
        full_url = dashboard_href.format(base_url=self.base_url)

        self.assertEqual(full_url, f"{self.base_url}/dashboard")

    def test_profile_url_construction_with_username(self):
        """Test profile URL construction with base_url and username placeholder."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]
        profile_href = profile_urls["profile"]["href"]

        # Step 1: Substitute base_url
        url_with_base = profile_href.format(base_url=self.base_url)
        self.assertIn(self.base_url, url_with_base)
        self.assertIn("(username)", url_with_base)

        # Step 2: The frontend should replace (username) with actual username
        full_url = url_with_base.replace("(username)", self.test_username)

        self.assertEqual(full_url, f"{self.base_url}/profile/u/{self.test_username}")
        self.assertNotIn("(username)", full_url)

    def test_account_url_construction(self):
        """Test account URL construction with base_url."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]
        account_href = profile_urls["account"]["href"]

        # Construct the full URL
        full_url = account_href.format(base_url=self.base_url)

        self.assertEqual(full_url, f"{self.base_url}/account/settings")

    def test_order_history_url_construction(self):
        """Test order history URL construction with base_url."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]
        order_history_href = profile_urls["order_history"]["href"]

        # Construct the full URL
        full_url = order_history_href.format(base_url=self.base_url)

        self.assertEqual(full_url, f"{self.base_url}/orders/orders")

    def test_all_urls_with_different_base_url(self):
        """Test that URLs work correctly with different base URLs."""
        custom_base = "https://custom-lms.university.edu"
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]

        expected_urls = {
            "dashboard": f"{custom_base}/dashboard",
            "account": f"{custom_base}/account/settings",
            "order_history": f"{custom_base}/orders/orders",
        }

        for key, expected_url in expected_urls.items():
            href = profile_urls[key]["href"]
            constructed_url = href.format(base_url=custom_base)
            self.assertEqual(constructed_url, expected_url)

    @override_settings(
        RICHIE_AUTHENTICATION_DELEGATION={
            **settings.RICHIE_AUTHENTICATION_DELEGATION,
            "BASE_URL": "https://openedx.example.com",
        }
    )
    def test_integration_with_base_url_setting(self):
        """Test integration with AUTHENTICATION_DELEGATION BASE_URL setting."""
        base_url_from_settings = settings.RICHIE_AUTHENTICATION_DELEGATION["BASE_URL"]
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]

        # Dashboard URL construction
        dashboard_url = profile_urls["dashboard"]["href"].format(
            base_url=base_url_from_settings
        )
        self.assertEqual(dashboard_url, "https://openedx.example.com/dashboard")

        # Profile URL construction
        profile_url = (
            profile_urls["profile"]["href"]
            .format(base_url=base_url_from_settings)
            .replace("(username)", self.test_username)
        )
        self.assertEqual(
            profile_url, f"https://openedx.example.com/profile/u/{self.test_username}"
        )

    def test_custom_url_patterns_integration(self):
        """Test that custom URL patterns work correctly when overridden."""
        custom_profile_urls = {
            "dashboard": {
                "label": "Dashboard",
                "href": "{base_url:s}/student/dashboard",
            },
            "profile": {
                "label": "Profile",
                "href": "{base_url:s}/users/(username)",
            },
            "account": {
                "label": "Account",
                "href": "{base_url:s}/settings/account",
            },
            "order_history": {
                "label": "Order History",
                "href": "{base_url:s}/commerce/orders",
            },
        }

        # Test each custom URL
        test_cases = [
            ("dashboard", f"{self.base_url}/student/dashboard"),
            (
                "profile",
                f"{self.base_url}/users/{self.test_username}",
            ),
            ("account", f"{self.base_url}/settings/account"),
            ("order_history", f"{self.base_url}/commerce/orders"),
        ]

        for key, expected_url in test_cases:
            href = custom_profile_urls[key]["href"]
            constructed_url = href.format(base_url=self.base_url)
            if "(username)" in constructed_url:
                constructed_url = constructed_url.replace(
                    "(username)", self.test_username
                )

            self.assertEqual(constructed_url, expected_url, f"Failed for {key}")

    def test_url_list_order_preservation(self):
        """Test that URL order is preserved for frontend display."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]

        # The order should match the definition order for consistent UI
        url_keys = list(profile_urls.keys())
        expected_order = ["dashboard", "profile", "account", "order_history"]

        self.assertEqual(url_keys, expected_order)
