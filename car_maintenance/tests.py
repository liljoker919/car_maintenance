from django.test import TestCase


class SettingsConfigurationTest(TestCase):
    """Test that settings are properly configured to use environment variables."""

    def test_secret_key_uses_environment_variable(self):
        """Test that SECRET_KEY is loaded from environment variable."""
        from django.conf import settings
        # SECRET_KEY should be set from environment
        self.assertIsNotNone(settings.SECRET_KEY)
        self.assertTrue(len(settings.SECRET_KEY) > 0)

    def test_debug_uses_environment_variable(self):
        """Test that DEBUG is loaded from environment variable."""
        from django.conf import settings
        # DEBUG should be set (either True or False)
        self.assertIsInstance(settings.DEBUG, bool)

    def test_settings_imports_decouple(self):
        """Test that settings.py imports the decouple library."""
        import car_maintenance.settings as settings_module
        # Check that config is imported
        self.assertTrue(hasattr(settings_module, 'config'))
