# core/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Profile, Post, Like, Commentary, Follower, Blocked

class CoreModelsTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.profile = Profile.objects.create(
            user=self.user,
            description="Test profile"
        )
        self.post = Post.objects.create(
            title="Test Post",
            body="Test content",
            owner=self.user
        )

    def test_profile_creation(self):
        """Test profile creation"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.description, "Test profile")
        self.assertEqual(str(self.profile), f"Profile of {self.user}")

    def test_post_creation(self):
        """Test post creation"""
        self.assertEqual(self.post.owner, self.user)
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(str(self.post), "Test Post")

    def test_like_creation(self):
        """Test like creation"""
        like = Like.objects.create(user=self.user, post=self.post)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.post, self.post)

    def test_comment_creation(self):
        """Test comment creation"""
        comment = Commentary.objects.create(
            user=self.user,
            post=self.post,
            body="Test comment"
        )
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.body, "Test comment")