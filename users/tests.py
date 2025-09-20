from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="pass1234"
        )

    # ----- Custom LoginView -----
    def test_custom_login_success(self):
        response = self.client.post(
            "/users/api/login/",
            {"username": "testuser", "password": "pass1234"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_custom_login_fail(self):
        response = self.client.post(
            "/users/api/login/",
            {"username": "wronguser", "password": "wrongpass"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    # ----- JWT TokenObtainPairView -----
    def test_jwt_login_success(self):
        response = self.client.post(
            "/users/api/token/",
            {"username": "testuser", "password": "pass1234"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())

    def test_jwt_login_fail(self):
        response = self.client.post(
            "/users/api/token/",
            {"username": "wronguser", "password": "wrongpass"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)
