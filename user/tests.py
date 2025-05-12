# user/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.models import User

class UserViewsTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.login_url = reverse("user:login")
        self.register_url = reverse("user:create")
        self.manage_url = reverse("user:manage")
        self.logout_url = reverse("user:logout")

    def test_user_registration(self):
        """Test user registration endpoint"""
        new_user_data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass123"
        }
        response = self.client.post(self.register_url, new_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_user_login(self):
        """Test user login endpoint"""
        response = self.client.post(self.login_url, {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_user_logout(self):
        """Test user logout endpoint"""
        # First login to get token
        login_response = self.client.post(self.login_url, {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        })
        token = login_response.data["token"]
        
        # Set token in header
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        
        # Test logout
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manage_user_profile(self):
        """Test user profile management"""
        # Login first
        login_response = self.client.post(self.login_url, {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        })
        token = login_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        # Test get profile
        response = self.client.get(self.manage_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user_data["username"])

        # Test update profile
        update_data = {"username": "updateduser"}
        response = self.client.patch(self.manage_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "updateduser")