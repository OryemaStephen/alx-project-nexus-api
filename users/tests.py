# ----- Custom LoginView -----
def test_custom_login_success(self):
    response = self.client.post(
        "/api/login/",
        {"username": "testuser", "password": "pass1234"},
        content_type="application/json",
    )
    self.assertEqual(response.status_code, 200)
    self.assertIn("message", response.json())

def test_custom_login_fail(self):
    response = self.client.post(
        "/api/login/",
        {"username": "wronguser", "password": "wrongpass"},
        content_type="application/json",
    )
    self.assertEqual(response.status_code, 400)
    self.assertIn("error", response.json())

# ----- JWT TokenObtainPairView -----
def test_jwt_login_success(self):
    response = self.client.post(
        "/api/token/",
        {"username": "testuser", "password": "pass1234"},
        content_type="application/json",
    )
    self.assertEqual(response.status_code, 200)
    self.assertIn("access", response.json())
    self.assertIn("refresh", response.json())

def test_jwt_login_fail(self):
    response = self.client.post(
        "/api/token/",
        {"username": "wronguser", "password": "wrongpass"},
        content_type="application/json",
    )
    self.assertEqual(response.status_code, 401)
