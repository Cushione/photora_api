from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User


class TestProfileModel(TestCase):
    """
    Tests for the Profile Model
    """

    def setUp(self):
        # Create Test User
        self.user = User.objects.create_user(
            username="testuser", password="12345"
        )

    def test_profile_created(self):
        profile = Profile.objects.get(owner=self.user)
        self.assertEqual(profile.name, "testuser")

    def test_image_defaults_to_placeholder(self):
        profile = Profile.objects.get(owner=self.user)
        self.assertIn("user_nbfhis", profile.image.url)

    def test_article_string_representation(self):
        profile = Profile.objects.get(owner=self.user)
        self.assertEqual(str(profile), "testuser's profile")
