from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class LoggingConfigurationTest(TestCase):
    """Test that logging is properly configured"""

    def test_logging_configuration_exists(self):
        """Test that LOGGING is configured in settings"""
        from django.conf import settings

        self.assertIn("LOGGING", dir(settings))
        self.assertIsInstance(settings.LOGGING, dict)
        self.assertEqual(settings.LOGGING["version"], 1)

    def test_logging_handlers_configured(self):
        """Test that file handler is configured"""
        from django.conf import settings

        self.assertIn("handlers", settings.LOGGING)
        self.assertIn("file", settings.LOGGING["handlers"])
        file_handler = settings.LOGGING["handlers"]["file"]
        self.assertEqual(file_handler["level"], "INFO")
        self.assertEqual(file_handler["class"], "logging.FileHandler")

    def test_logging_loggers_configured(self):
        """Test that loggers are configured for each app"""
        from django.conf import settings

        self.assertIn("loggers", settings.LOGGING)
        loggers = settings.LOGGING["loggers"]

        # Check django logger
        self.assertIn("django", loggers)
        self.assertEqual(loggers["django"]["level"], "INFO")

        # Check app loggers
        for app in ["vehicles", "compliance", "insurance", "registration"]:
            self.assertIn(app, loggers)
            self.assertEqual(loggers[app]["level"], "DEBUG")
            self.assertIn("file", loggers[app]["handlers"])

    def test_log_file_path_is_valid(self):
        """Test that log file path is correctly configured"""
        from django.conf import settings
        import os

        log_path = settings.LOGGING["handlers"]["file"]["filename"]
        log_dir = os.path.dirname(log_path)

        # Check that path contains 'logs' directory
        self.assertIn("logs", log_path)

        # Verify the log directory basename is 'logs'
        self.assertEqual(os.path.basename(log_dir), "logs")


class LoggingFunctionalityTest(TestCase):
    """Test that logging is working in views"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_user_registration_logs(self):
        """Test that user registration generates a log entry"""
        self.client.logout()

        with self.assertLogs("registration", level="INFO") as cm:
            self.client.post(
                reverse("register"),
                {
                    "username": "newuser",
                    "email": "newuser@test.com",
                    "password1": "testpass123456",
                    "password2": "testpass123456",
                },
            )

            # Check that log was created
            self.assertTrue(any("New user registered" in log for log in cm.output))
            self.assertTrue(any("newuser" in log for log in cm.output))

    def test_vehicle_creation_logs_with_valid_data(self):
        """Test that creating a vehicle with valid data generates log"""
        with self.assertLogs("vehicles", level="INFO") as cm:
            # Post with all required fields to ensure success
            self.client.post(
                reverse("vehicles:vehicle_add"),
                {
                    "make": "Toyota",
                    "model": "Camry",
                    "year": 2020,
                    "current_mileage": 25000,
                    "vin": "1HGBH41JXMN109186",
                    "condition": "good",
                },
                follow=True,
            )

            # Check that log was created
            self.assertTrue(any("created new vehicle" in log for log in cm.output))
            self.assertTrue(any("testuser" in log for log in cm.output))
