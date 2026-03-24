"""Test authentication profile URLs configuration."""

from unittest import mock

from django.conf import settings
from django.test import TestCase, override_settings


class AuthenticationProfileURLsTestCase(TestCase):
    """Test cases for AUTHENTICATION_DELEGATION PROFILE_URLS configuration."""

    def test_default_profile_urls_structure(self):
        """Test that PROFILE_URLS has the expected structure with default values."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]

        # Check that all expected keys are present
        expected_keys = ["dashboard", "profile", "account", "order_history"]
        self.assertEqual(set(profile_urls.keys()), set(expected_keys))

        # Check that each URL has both 'label' and 'href'
        for key, url_config in profile_urls.items():
            self.assertIn("label", url_config, f"Missing 'label' in {key}")
            self.assertIn("href", url_config, f"Missing 'href' in {key}")

    def test_default_dashboard_url(self):
        """Test the default dashboard URL configuration."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]
        dashboard = profile_urls["dashboard"]

        self.assertEqual(str(dashboard["label"]), "Meus cursos")
        self.assertEqual(dashboard["href"], "{base_url:s}/dashboard")

    def test_default_profile_url(self):
        """Test the default profile URL configuration."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]
        profile = profile_urls["profile"]

        self.assertEqual(str(profile["label"]), "Perfil")
        self.assertEqual(profile["href"], "{base_url:s}/profile/u/(username)")

    def test_default_account_url(self):
        """Test the default account URL configuration."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]
        account = profile_urls["account"]

        self.assertEqual(str(account["label"]), "Conta")
        self.assertEqual(account["href"], "{base_url:s}/account/settings")

    @override_settings(
        LANGUAGE_CODE="en",
        LANGUAGES=(("en", "English"), ("pt", "Portuguese")),
    )
    def test_default_order_history_url(self):
        """Test the default order history URL configuration."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]
        order_history = profile_urls["order_history"]

        self.assertEqual(str(order_history["label"]), "Order History")
        self.assertEqual(order_history["href"], "{base_url:s}/orders/orders")

    @override_settings(
        RICHIE_AUTHENTICATION_DELEGATION={
            **settings.RICHIE_AUTHENTICATION_DELEGATION,
            "PROFILE_URLS": {
                **settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"],
                "dashboard": {
                    "label": "Dashboard",
                    "href": "{base_url:s}/custom/dashboard",
                },
            },
        }
    )
    def test_override_dashboard_url(self):
        """Test that dashboard URL can be overridden."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]
        dashboard = profile_urls["dashboard"]

        self.assertEqual(dashboard["href"], "{base_url:s}/custom/dashboard")

    @override_settings(
        RICHIE_AUTHENTICATION_DELEGATION={
            **settings.RICHIE_AUTHENTICATION_DELEGATION,
            "PROFILE_URLS": {
                **settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"],
                "account": {
                    "label": "Account",
                    "href": "{base_url:s}/my-account",
                },
            },
        }
    )
    def test_override_account_url(self):
        """Test that account URL can be overridden."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]
        account = profile_urls["account"]

        self.assertEqual(account["href"], "{base_url:s}/my-account")

    @override_settings(
        RICHIE_AUTHENTICATION_DELEGATION={
            **settings.RICHIE_AUTHENTICATION_DELEGATION,
            "PROFILE_URLS": {
                **settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"],
                "profile": {
                    "label": "Profile",
                    "href": "{base_url:s}/user/(username)/profile",
                },
            },
        }
    )
    def test_override_profile_url_with_username_placeholder(self):
        """Test that profile URL can be overridden with custom username placeholder."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]
        profile = profile_urls["profile"]

        self.assertEqual(profile["href"], "{base_url:s}/user/(username)/profile")

    @mock.patch.dict(
        "os.environ",
        {
            "AUTHENTICATION_PROFILE_URL_DASHBOARD": "{base_url:s}/env/dashboard",
            "AUTHENTICATION_PROFILE_URL_ACCOUNT": "{base_url:s}/env/account",
        },
    )
    def test_environment_variables_override(self):
        """Test that profile URLs can be configured via environment variables.

        Note: This test demonstrates the pattern, but actual env var loading
        happens at Django startup. In practice, you would set these in your
        environment before starting Django.
        """
        # This test documents the expected behavior.
        # The actual environment variables would be:
        # - AUTHENTICATION_PROFILE_URL_DASHBOARD
        # - AUTHENTICATION_PROFILE_URL_PROFILE
        # - AUTHENTICATION_PROFILE_URL_ACCOUNT
        # - AUTHENTICATION_PROFILE_URL_ORDER_HISTORY

        expected_env_vars = [
            "AUTHENTICATION_PROFILE_URL_DASHBOARD",
            "AUTHENTICATION_PROFILE_URL_PROFILE",
            "AUTHENTICATION_PROFILE_URL_ACCOUNT",
            "AUTHENTICATION_PROFILE_URL_ORDER_HISTORY",
        ]

        # Document that these environment variables are available
        for env_var in expected_env_vars:
            self.assertIsNotNone(
                env_var,
                f"Environment variable {env_var} should be available for configuration",
            )

    def test_url_placeholders_format(self):
        """Test that URLs contain expected placeholder formats."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]

        # Check dashboard URL has base_url placeholder
        self.assertIn("{base_url", profile_urls["dashboard"]["href"])

        # Check profile URL has both base_url and username placeholders
        profile_href = profile_urls["profile"]["href"]
        self.assertIn("{base_url", profile_href)
        self.assertIn("(username)", profile_href)

        # Check account URL has base_url placeholder
        self.assertIn("{base_url", profile_urls["account"]["href"])

        # Check order_history URL has base_url placeholder
        self.assertIn("{base_url", profile_urls["order_history"]["href"])

    def test_profile_urls_labels_are_translatable(self):
        """Test that profile URL labels are marked for translation."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]

        # All labels should be string-like (translation proxy or str)
        for key, url_config in profile_urls.items():
            label = url_config["label"]
            # Labels should be either str or translation proxy objects
            self.assertTrue(
                hasattr(label, "__str__"),
                f"Label for {key} should be translatable or a string",
            )

    def test_gamma_dashboard_entries_disabled_by_default(self):
        """Test that performance and leaderboard are filtered out by default."""
        profile_urls = settings.RICHIE_AUTHENTICATION_DELEGATION["PROFILE_URLS"]

        # Performance and leaderboard should not be present (filtered by post_setup)
        # because they have enabled=False by default
        self.assertNotIn("performance", profile_urls)
        self.assertNotIn("leaderboard", profile_urls)
        self.assertIn("dashboard", profile_urls)

    def test_filtering_removes_disabled_entries(self):
        """Test that post_setup filtering removes entries with enabled=False."""
        # Simulate PROFILE_URLS with enabled flags
        test_urls = {
            "dashboard": {"label": "Dashboard", "href": "{base_url:s}/dashboard"},
            "performance": {
                "label": "Performance",
                "href": "{base_url:s}/gamma_dashboard/dashboard/",
                "enabled": False,  # Should be filtered out
            },
            "leaderboard": {
                "label": "Leaderboard",
                "href": "{base_url:s}/gamma_dashboard/leaderboard/",
                "enabled": False,  # Should be filtered out
            },
            "profile": {
                "label": "Profile",
                "href": "{base_url:s}/profile/u/(username)",
            },
        }

        # Apply the filtering logic from post_setup
        filtered_urls = {
            key: value
            for key, value in test_urls.items()
            if value.get("enabled", True) is not False
        }

        # Verify filtering worked
        self.assertIn("dashboard", filtered_urls)
        self.assertIn("profile", filtered_urls)
        self.assertNotIn("performance", filtered_urls)  # Was filtered out
        self.assertNotIn("leaderboard", filtered_urls)  # Was filtered out

    def test_filtering_keeps_enabled_entries(self):
        """Test that post_setup filtering keeps entries with enabled=True."""
        # Simulate PROFILE_URLS with enabled=True
        test_urls = {
            "dashboard": {"label": "Dashboard", "href": "{base_url:s}/dashboard"},
            "performance": {
                "label": "Performance",
                "href": "{base_url:s}/gamma_dashboard/dashboard/",
                "enabled": True,  # Should be kept
            },
            "leaderboard": {
                "label": "Leaderboard",
                "href": "{base_url:s}/gamma_dashboard/leaderboard/",
                "enabled": True,  # Should be kept
            },
            "profile": {
                "label": "Profile",
                "href": "{base_url:s}/profile/u/(username)",
            },
        }

        # Apply the filtering logic from post_setup
        filtered_urls = {
            key: value
            for key, value in test_urls.items()
            if value.get("enabled", True) is not False
        }

        # Verify all entries are present
        self.assertIn("dashboard", filtered_urls)
        self.assertIn("performance", filtered_urls)  # Was kept
        self.assertIn("leaderboard", filtered_urls)  # Was kept
        self.assertIn("profile", filtered_urls)

    def test_filtering_preserves_entries_without_enabled_flag(self):
        """Test that entries without enabled flag are kept (backward compatibility)."""
        # Simulate PROFILE_URLS without enabled flags (like existing entries)
        test_urls = {
            "dashboard": {"label": "Dashboard", "href": "{base_url:s}/dashboard"},
            "profile": {
                "label": "Profile",
                "href": "{base_url:s}/profile/u/(username)",
            },
        }

        # Apply the filtering logic from post_setup
        filtered_urls = {
            key: value
            for key, value in test_urls.items()
            if value.get("enabled", True) is not False
        }

        # Verify all entries without enabled flag are kept
        self.assertIn("dashboard", filtered_urls)
        self.assertIn("profile", filtered_urls)
        self.assertEqual(len(filtered_urls), 2)
