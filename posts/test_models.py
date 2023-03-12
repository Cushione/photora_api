from django.test import TestCase
from .models import Post
from django.contrib.auth.models import User


class TestPostModel(TestCase):
    """
    Tests for the Post Model
    """

    def setUp(self):
        # Create Test User
        self.user = User.objects.create_user(
            username="testuser", password="12345"
        )

        # Create Test Post
        self.post = Post.objects.create(
            title="Test Post", owner=self.user, description="Test Description"
        )

    def test_post_has_number_of_likes(self):
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.number_of_likes(), 0)
        post.likes.add(self.user)
        self.assertEqual(post.number_of_likes(), 1)

    def test_article_has_number_of_comments(self):
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.number_of_comments(), 0)

    def test_article_string_representation(self):
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(str(post), "Test Post")
